from app_manager.elastic_manager.elastic_controller import elastic_controller
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.constants.strings import GENERAL_STRINGS
from trustly.controllers.helper_manager.helper_controller import helper_controller
from trustly.controllers.view_managers.user.interactive.hompage_manager.homepage_enums import HOMEPAGE_CALLBACK, HOMEPAGE_PARAM, HOMEPAGE_SESSION_COMMANDS
from app_manager.request_manager.request_handler import request_handler
from app_manager.elastic_manager.elastic_enums import ELASTIC_CRUD_COMMANDS, ELASTIC_REQUEST_COMMANDS, ELASTIC_KEYS


class homepage_session_controller(request_handler):

    # Helper Methods
    def __init_parameters(self, p_data):
        import json

        results_dict = {}
        try:
            m_status, m_documents = elastic_controller.get_instance().invoke_trigger(
                ELASTIC_CRUD_COMMANDS.S_INSIGHT,
                [ELASTIC_REQUEST_COMMANDS.S_GENERATE_INSIGHT, [], [None]]
            )

            results = []

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
                                results.append({
                                    "query_type": query_type,
                                    agg_name: agg_value.get("value", "N/A")
                                })
                        else:
                            hits = result_body.get("hits", {})
                            if "total" in hits:
                                results.append({
                                    "query_type": query_type,
                                    "total_documents": hits["total"].get("value", "N/A")
                                })
                    elif error:
                        results.append({
                            "query_type": query_type,
                            "error": error
                        })
            results_dict = json.dumps(results, indent=4)

        except Exception as e:
            print(json.dumps({"error": str(e)}, indent=4))

        results_dict = json.loads(results_dict)
        m_context = {
            HOMEPAGE_CALLBACK.M_REFERENCE: helper_controller.load_json(CONSTANTS.S_REFERENCE_WEBSITE_URL),
            HOMEPAGE_CALLBACK.M_SECURE_SERVICE_NOTICE: GENERAL_STRINGS.S_GENERAL_HTTP,
            HOMEPAGE_CALLBACK.M_STATISTICS: results_dict
        }

        if HOMEPAGE_PARAM.M_SECURE_SERVICE in p_data.GET:
            m_context[HOMEPAGE_CALLBACK.M_SECURE_SERVICE_NOTICE] = p_data.GET[HOMEPAGE_PARAM.M_SECURE_SERVICE]

        return m_context, True

    # External Request Callbacks
    def invoke_trigger(self, p_command, p_data):
        if p_command == HOMEPAGE_SESSION_COMMANDS.M_INIT:
            return self.__init_parameters(p_data)