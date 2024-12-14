from trustly.app.view_managers.interactive.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from trustly.app.view_managers.interactive.directory_manager.directory_view_model import directory_view_model
from trustly.management.managers.insight_job import insight_job


def get_directory(request):
  return directory_view_model.getInstance().invoke_trigger(DIRECTORY_MODEL_COMMANDS.M_FETCH_LIST, request)


def get_insight(request):
  return insight_job.get_instance().get_trending_insights()


def get_results(request):
  return None
