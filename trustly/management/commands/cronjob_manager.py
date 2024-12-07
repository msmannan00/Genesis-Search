from django.core.management.base import BaseCommand

from trustly.management.managers.insight_job import insight_job
from trustly.services.elastic_manager.elastic_controller import elastic_controller
from trustly.controllers.constants.constant import CONSTANTS
from trustly.management.commands.scheduler import RepeatedTimer
from trustly.services.redis_manager.redis_controller import redis_controller
from trustly.services.redis_manager.redis_enums import REDIS_COMMANDS, REDIS_KEYS, REDIS_DEFAULT

class Command(BaseCommand):

    @staticmethod
    def init_handles():
        insight_old = redis_controller().invoke_trigger(REDIS_COMMANDS.S_GET_STRING, [REDIS_KEYS.INSIGHT_NEW_DAY, REDIS_DEFAULT.INSIGHT_DEFAULT, None])
        if str(insight_old) == str(REDIS_DEFAULT.INSIGHT_DEFAULT):
            insight_job.get_instance().init_trending_insights_daily()
            insight_job.get_instance().init_trending_insights_weekly()

    def handle(self, *args, **kwargs):
        self.init_handles()

        RepeatedTimer(CONSTANTS.S_SETTINGS_INDEX_EXPIRY_TIMEOUT, elastic_controller.get_instance().purge_old_records, False)
        RepeatedTimer(CONSTANTS.S_SETTINGS_INDEX_STATS_DAILY_TIMEOUT, insight_job.get_instance().init_trending_insights_daily, False)
        RepeatedTimer(CONSTANTS.S_SETTINGS_INDEX_STATS_WEEKLY_TIMEOUT, insight_job.get_instance().init_trending_insights_weekly, False)
