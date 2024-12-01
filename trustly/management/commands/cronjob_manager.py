from django.core.management.base import BaseCommand

from trustly.management.managers.insight_job import insight_job
from trustly.services.elastic_manager.elastic_controller import elastic_controller
from trustly.controllers.constants.constant import CONSTANTS
from trustly.management.commands.scheduler import RepeatedTimer


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        RepeatedTimer(CONSTANTS.S_SETTINGS_INDEX_EXPIRY_TIMEOUT, elastic_controller.get_instance().purge_old_records, False)
        RepeatedTimer(CONSTANTS.S_SETTINGS_INDEX_EXPIRY_TIMEOUT, insight_job.get_instance().init_trending_insights, True)
