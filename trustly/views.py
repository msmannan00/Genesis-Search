from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from trustly.services.block_manager.block_controller import block_controller
from trustly.services.user_auth_manager.user_auth_controller import user_auth_controller
from trustly.services.user_auth_manager.user_auth_enums import USER_AUTH_COMMANDS
from trustly.controllers.constants.constant import CONSTANTS
from trustly.controllers.server_manager.crawl_index_manager.crawl_controller import crawl_controller
from trustly.controllers.server_manager.crawl_index_manager.crawl_enums import CRAWL_COMMANDS
from trustly.controllers.server_manager.external_request_manager.external_request_controller import external_request_controller
from trustly.controllers.server_manager.external_request_manager.external_request_enums import EXTERNAL_REQUEST_COMMANDS
from trustly.controllers.view_managers.cms.dashboard.dashboard_view_model import dashboard_view_model
from trustly.controllers.view_managers.cms.dashboard.dashboard_enums import DASHBOARD_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.login.login_view_model import login_view_model
from trustly.controllers.view_managers.cms.login.login_enums import LOGIN_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.manage_search.manage_search_view_model import manage_search_view_model
from trustly.controllers.view_managers.cms.manage_search.manage_search_enums import MANAGE_SEARCH_MODEL_CALLBACK
from trustly.controllers.view_managers.cms.manage_status.manage_status_view_model import manage_status_view_model
from trustly.controllers.view_managers.cms.manage_status.manage_status_enums import MANAGE_STATUS_MODEL_CALLBACK
from trustly.controllers.view_managers.user.server.block_manager.block_enums import BLOCK_MODEL_CALLBACK
from trustly.controllers.view_managers.user.server.error.error_view_model import error_view_model
from trustly.controllers.view_managers.user.server.error.error_enums import ERROR_MODEL_CALLBACK
from trustly.controllers.view_managers.user.server.secret_key.secret_key_view_model import secret_key_view_model
from trustly.controllers.view_managers.user.server.secret_key.secret_key_enums import SECRET_KEY_MODEL_CALLBACK
from trustly.controllers.view_managers.user.interactive.directory_manager.directory_view_model import directory_view_model
from trustly.controllers.view_managers.user.interactive.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.hompage_manager.homepage_view_model import homepage_view_model
from trustly.controllers.view_managers.user.interactive.hompage_manager.homepage_enums import HOMEPAGE_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.notice_manager.notice_view_model import notice_view_model
from trustly.controllers.view_managers.user.interactive.notice_manager.notice_enums import NOTICE_MODEL_CALLBACK
from trustly.controllers.view_managers.user.interactive.policy_manager.policy_view_model import policy_view_model
from trustly.controllers.view_managers.user.interactive.policy_manager.policy_enums import POLICY_MODEL_CALLBACK
from trustly.controllers.view_managers.user.interactive.report_manager.report_view_model import report_view_model
from trustly.controllers.view_managers.user.interactive.report_manager.report_enums import REPORT_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.search_manager.search_view_model import search_view_model
from trustly.controllers.view_managers.user.interactive.search_manager.search_enums import SEARCH_MODEL_COMMANDS
from trustly.controllers.view_managers.user.interactive.sitemap_manager.sitemap_view_model import sitemap_view_model
from trustly.controllers.view_managers.user.interactive.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS
def index(request):
  return homepage_view_model.getInstance().invoke_trigger(HOMEPAGE_MODEL_COMMANDS.M_INIT, request)

def command(request):
  return homepage_view_model.getInstance().invoke_trigger(HOMEPAGE_MODEL_COMMANDS.M_INIT, request)

def privacy(request):
  return policy_view_model.getInstance().invoke_trigger(POLICY_MODEL_CALLBACK.M_INIT, request)

@ensure_csrf_cookie
def report(request):
  return report_view_model.getInstance().invoke_trigger(REPORT_MODEL_COMMANDS.M_INIT, request)

def notice(request):
  return notice_view_model.getInstance().invoke_trigger(NOTICE_MODEL_CALLBACK.M_INIT, request)

@ensure_csrf_cookie
def sitemap(request):
  return sitemap_view_model.getInstance().invoke_trigger(SITEMAP_MODEL_COMMANDS.M_INIT, request)

def secretkey(request):
  return secret_key_view_model.getInstance().invoke_trigger(SECRET_KEY_MODEL_CALLBACK.M_INIT, request)

def directory(request):
  return directory_view_model.getInstance().invoke_trigger(DIRECTORY_MODEL_COMMANDS.M_INIT, request)

def search(request):
  return search_view_model.getInstance().invoke_trigger(SEARCH_MODEL_COMMANDS.M_INIT, request)

def parser(request):
  return crawl_controller.getInstance().invoke_trigger(CRAWL_COMMANDS.M_FETCH_PARSER, request)

def feeder_unique(request):
  return crawl_controller.getInstance().invoke_trigger(CRAWL_COMMANDS.M_FETCH_FEEDER_UNIQUE, request)

def feeder_publish(request):
  return crawl_controller.getInstance().invoke_trigger(CRAWL_COMMANDS.M_FETCH_FEEDER_PUBLISH, request)

def feeder(request):
  return crawl_controller.getInstance().invoke_trigger(CRAWL_COMMANDS.M_FETCH_FEEDER, request)

def block(request):
  return block_controller.getInstance().invoke_trigger(BLOCK_MODEL_CALLBACK.M_INIT, request)

def restricted_static(request):
  return render(None, CONSTANTS.S_TEMPLATE_RESTRICTED_WEBSITE_PATH)

@ensure_csrf_cookie
def cms_login(request):
  return login_view_model.getInstance().invoke_trigger(LOGIN_MODEL_CALLBACK.M_INIT, request)

def manage_status(request):
  return manage_status_view_model.getInstance().invoke_trigger(MANAGE_STATUS_MODEL_CALLBACK.M_INIT, request)

def manage_search(request):
  if request.method == 'GET':
    return manage_search_view_model.getInstance().invoke_trigger(MANAGE_SEARCH_MODEL_CALLBACK.M_INIT, request)
  elif request.method == 'POST':
    return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH, None)

@csrf_exempt
def crawl_index(request):
  return crawl_controller.getInstance().invoke_trigger(CRAWL_COMMANDS.M_INIT, request)

@csrf_protect
def manage_authentication(request):
  return user_auth_controller.getInstance().invoke_trigger(USER_AUTH_COMMANDS.M_AUTHENTICATE, request)

def update_status(request):
  return external_request_controller.getInstance().invoke_trigger(EXTERNAL_REQUEST_COMMANDS.M_UPDATE_MODULE_STATUS, request)

def manage_logout(request):
  return user_auth_controller.getInstance().invoke_trigger(USER_AUTH_COMMANDS.M_LOGOUT, request)

def cms_dashboard(request):
  return dashboard_view_model.getInstance().invoke_trigger(DASHBOARD_MODEL_CALLBACK.M_INIT, request)

def error_page_400(request, exception=None):
  return error_view_model.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 400])

def error_page_403(request, exception=None):
  return error_view_model.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 403])

def error_page_404(request, exception, template_name='trustly/error/error.html'):
  return error_view_model.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 404])

def error_page_500(request, exception=None):
  return error_view_model.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 500])
