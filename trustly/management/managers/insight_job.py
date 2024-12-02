from datetime import datetime, timezone

from trustly.services.elastic_manager.elastic_controller import elastic_controller
from trustly.services.elastic_manager.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS, ELASTIC_KEYS
from trustly.services.redis_manager.redis_controller import redis_controller
from trustly.services.redis_manager.redis_enums import REDIS_COMMANDS, REDIS_KEYS, REDIS_DEFAULT
from trustly.services.request_manager.request_handler import request_handler


class insight_job(request_handler):
    __instance = None

    # Initializations
    @staticmethod
    def get_instance():
        if insight_job.__instance is None:
            insight_job()
        return insight_job.__instance

    def __init__(self):
        if insight_job.__instance is not None:
            pass
        else:
            insight_job.__instance = self
            self.__m_session = insight_job()

    @staticmethod
    def __fetch_elastic_insight(grouped_results):
        m_status, m_documents = elastic_controller.get_instance().invoke_trigger(
            ELASTIC_CRUD_COMMANDS.S_INSIGHT,
            [ELASTIC_REQUEST_COMMANDS.S_GENERATE_INSIGHT, [], [None]]
        )

        if m_status and isinstance(m_documents, list):
            for doc in m_documents:
                query_type = doc.get("query", {}).get(ELASTIC_KEYS.S_DOCUMENT, "unknown")
                result = doc.get("result", None)
                error = doc.get("error", None)

                if result:
                    result_body = result.body if hasattr(result, 'body') else result
                    aggregations = result_body.get("aggregations", {})
                    if aggregations:
                        for agg_name, agg_value in aggregations.items():
                            if agg_name in ["Most Recent", "Oldest Update"]:
                                epoch_value = agg_value.get("value", None)
                                epoch_value = epoch_value or 0
                                if epoch_value:
                                    date_value = datetime.fromtimestamp(epoch_value / 1000, timezone.utc).strftime("%d %b")
                                    grouped_results[query_type].append({agg_name: date_value})
                                else:
                                    grouped_results[query_type].append({agg_name: "0"})
                            elif agg_name == "Common Type":
                                # Handle Common Type explicitly for terms aggregation
                                buckets = agg_value.get("buckets", [])
                                if buckets:
                                    # Extract the key of the most common type
                                    most_common_type = buckets[0].get("key", "general")
                                    grouped_results[query_type].append({agg_name: most_common_type})
                                else:
                                    grouped_results[query_type].append({agg_name: "general"})
                            else:
                                value = agg_value.get("value", None) or 0
                                grouped_results[query_type].append({agg_name: value})
                elif error:
                    grouped_results[query_type].append({"error": error})

        return grouped_results

    @staticmethod
    def generate_insight_comparison(insight_old, insight_new):
        try:
            old_data = eval(insight_old)
            new_data = eval(insight_new)

            comparison_result = {"generic_model": [], "leak_model": []}

            for key in ["generic_model", "leak_model"]:
                old_entries = {
                    list(entry.keys())[0]: list(entry.values())[0]
                    for entry in old_data.get(key, [])
                    if isinstance(entry, dict) and entry
                }
                new_entries = {
                    list(entry.keys())[0]: list(entry.values())[0]
                    for entry in new_data.get(key, [])
                    if isinstance(entry, dict) and entry
                }

                all_metrics = set(old_entries.keys()).union(set(new_entries.keys()))

                for metric in all_metrics:
                    new_value = new_entries.get(metric, 0)
                    old_value = old_entries.get(metric, 0)

                    if isinstance(new_value, (int, float)):
                        new_value = round(new_value, 5)
                    if isinstance(old_value, (int, float)):
                        old_value = round(old_value, 5)

                    if isinstance(new_value, (int, float)) and isinstance(old_value, (int, float)):
                        if old_value == 0:
                            change_percentage = new_value
                        else:
                            change_percentage = ((new_value - old_value) / abs(old_value)) * 100

                        formatted_change = f"{round(change_percentage, 2):+.2f}%"
                        comparison_result[key].append({
                            metric: {
                                "value": new_value,
                                "change": formatted_change
                            }
                        })
                    else:
                        comparison_result[key].append({
                            metric: {
                                "value": new_value,
                                "change": "-"
                            }
                        })

            return str(comparison_result)

        except Exception as e:
            return f"Error processing insights: {str(e)}"

    def init_trending_insights(self):
        results_dict, grouped_results = {}, {"generic_model": [], "leak_model": []}

        try:
            results_dict = self.__fetch_elastic_insight(grouped_results)
        except Exception as e:
            results_dict = {"error": str(e)}

        insight_old = redis_controller().invoke_trigger(
            REDIS_COMMANDS.S_GET_STRING,
            [REDIS_KEYS.INSIGHT_OLD, REDIS_DEFAULT.INSIGHT_DEFAULT, None]
        )

        insight_new = str(results_dict)
        trending_insight = self.generate_insight_comparison(insight_old, insight_new)

        redis_controller().invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [REDIS_KEYS.INSIGHT_OLD, insight_new, None])
        redis_controller().invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [REDIS_KEYS.INSIGHT_NEW, insight_new, None])
        redis_controller().invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [REDIS_KEYS.INSIGHT_STAT, trending_insight, None])

