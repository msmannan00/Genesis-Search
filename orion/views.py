from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from orion.controllers.constants.constant import CONSTANTS
from orion.controllers.server_manager.crawl_manager.crawl_controller import crawl_controller
from orion.controllers.server_manager.crawl_manager.crawl_enums import CRAWL_COMMANDS
from orion.controllers.server_manager.external_request_manager.external_request_controller import \
    external_request_controller
from orion.controllers.server_manager.external_request_manager.external_request_enums import EXTERNAL_REQUEST_COMMANDS
from orion.controllers.server_manager.user_auth_manager.user_auth_controller import user_auth_controller
from orion.controllers.server_manager.user_auth_manager.user_auth_enums import USER_AUTH_COMMANDS
from orion.controllers.view_managers.advert.advert_controller import advert_controller
from orion.controllers.view_managers.advert.advert_enums import ADVERT_MODEL_COMMANDS
from orion.controllers.view_managers.cms.dashboard.dashboard_controller import dashboard_controller
from orion.controllers.view_managers.cms.dashboard.dashboard_enums import DASHBOARD_MODEL_CALLBACK
from orion.controllers.view_managers.cms.login.login_controller import login_controller
from orion.controllers.view_managers.cms.login.login_enums import LOGIN_MODEL_CALLBACK
from orion.controllers.view_managers.cms.manage_search.manage_search_controller import manage_search_controller
from orion.controllers.view_managers.cms.manage_search.manage_search_enums import MANAGE_SEARCH_MODEL_CALLBACK
from orion.controllers.view_managers.cms.manage_status.manage_status_controller import manage_status_controller
from orion.controllers.view_managers.cms.manage_status.manage_status_enums import MANAGE_STATUS_MODEL_CALLBACK
from orion.controllers.view_managers.user.interactive.intelligence_manager.intelligence_controller import \
    intelligence_controller
from orion.controllers.view_managers.user.interactive.intelligence_manager.intelligence_enums import \
    INTELLIGENCE_MODEL_COMMANDS
from orion.controllers.view_managers.user.server.block_manager.block_enums import BLOCK_MODEL_CALLBACK
from orion.controllers.view_managers.user.server.error.error_controller import error_controller
from orion.controllers.view_managers.user.server.error.error_enums import ERROR_MODEL_CALLBACK
from orion.controllers.view_managers.user.server.maintenance.maintenance_controller import maintenance_controller
from orion.controllers.view_managers.user.server.maintenance.maintenance_enums import MAINTENANCE_MODEL_CALLBACK
from orion.controllers.view_managers.user.server.secret_key.secret_key_controller import secret_key_controller
from orion.controllers.view_managers.user.server.secret_key.secret_key_enums import SECRET_KEY_MODEL_CALLBACK
from orion.controllers.view_managers.user.server.user_index_manager.user_index_controller import user_index_controller
from orion.controllers.view_managers.user.server.user_index_manager.user_index_enums import USER_INDEX_MODEL_CALLBACK
from orion.controllers.view_managers.user.interactive.directory_manager.directory_controller import directory_controller
from orion.controllers.view_managers.user.interactive.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from orion.controllers.view_managers.user.interactive.hompage_manager.homepage_controller import homepage_controller
from orion.controllers.view_managers.user.interactive.hompage_manager.homepage_enums import HOMEPAGE_MODEL_COMMANDS
from orion.controllers.view_managers.user.interactive.notice_manager.notice_controller import notice_controller
from orion.controllers.view_managers.user.interactive.notice_manager.notice_enums import NOTICE_MODEL_CALLBACK
from orion.controllers.view_managers.user.interactive.policy_manager.policy_controller import policy_controller
from orion.controllers.view_managers.user.interactive.policy_manager.policy_enums import POLICY_MODEL_CALLBACK
from orion.controllers.view_managers.user.interactive.report_manager.report_controller import report_controller
from orion.controllers.view_managers.user.interactive.report_manager.report_enums import REPORT_MODEL_COMMANDS
from orion.controllers.view_managers.user.interactive.search_manager.search_controller import search_controller
from orion.controllers.view_managers.user.interactive.search_manager.search_enums import SEARCH_MODEL_COMMANDS
from orion.controllers.view_managers.user.interactive.sitemap_manager.sitemap_controller import sitemap_controller
from orion.controllers.view_managers.user.interactive.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS
from shared_directory.service_manager.block_manager.block_controller import block_controller


def index(request):
    return homepage_controller.getInstance().invoke_trigger(HOMEPAGE_MODEL_COMMANDS.M_INIT, request)


@csrf_exempt
def command(request):
    return homepage_controller.getInstance().invoke_trigger(HOMEPAGE_MODEL_COMMANDS.M_INIT, request)


@csrf_exempt
def privacy(request):
    return policy_controller.getInstance().invoke_trigger(POLICY_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def report(request):
    return report_controller.getInstance().invoke_trigger(REPORT_MODEL_COMMANDS.M_INIT, request)


@csrf_exempt
def notice(request):
    return notice_controller.getInstance().invoke_trigger(NOTICE_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def sitemap(request):
    return sitemap_controller.getInstance().invoke_trigger(SITEMAP_MODEL_COMMANDS.M_INIT, request)


@csrf_exempt
def secretkey(request):
    return secret_key_controller.getInstance().invoke_trigger(SECRET_KEY_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def directory(request):
    return directory_controller.getInstance().invoke_trigger(DIRECTORY_MODEL_COMMANDS.M_INIT, request)


@csrf_exempt
def search(request):
    return search_controller.getInstance().invoke_trigger(SEARCH_MODEL_COMMANDS.M_INIT, request)


@csrf_exempt
def user_index(request):
    return user_index_controller.getInstance().invoke_trigger(USER_INDEX_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def test(request):
    return render(None, CONSTANTS.S_SSL_VERIFICATION_PATH)


@csrf_exempt
def crawl_index(request):
    return crawl_controller.getInstance().invoke_trigger(CRAWL_COMMANDS.M_INIT, request)


@csrf_exempt
def intelligence(request):
    return intelligence_controller.getInstance().invoke_trigger(INTELLIGENCE_MODEL_COMMANDS.M_INIT, request)


@csrf_exempt
def download(request):
    return render(None, CONSTANTS.S_TEMPLATE_DOWNLOAD_WEBSITE_PATH)


@csrf_exempt
def maintenance(request):
    return maintenance_controller.getInstance().invoke_trigger(MAINTENANCE_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def ssl_validation(request):
    return render(None, CONSTANTS.S_SSL_VERIFICATION_PATH)


@csrf_exempt
def block(request):
    return block_controller.getInstance().invoke_trigger(BLOCK_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def block_static(request):
    return render(None, CONSTANTS.S_TEMPLATE_BLOCK_WEBSITE_PATH)


@csrf_exempt
def cms_login(request):
    return login_controller.getInstance().invoke_trigger(LOGIN_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def manage_status(request):
    return manage_status_controller.getInstance().invoke_trigger(MANAGE_STATUS_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def manage_search(request):
    return manage_search_controller.getInstance().invoke_trigger(MANAGE_SEARCH_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def manage_authentication(request):
    return user_auth_controller.getInstance().invoke_trigger(USER_AUTH_COMMANDS.M_AUTHENTICATE, request)


@csrf_exempt
def update_status(request):
    return external_request_controller.getInstance().invoke_trigger(EXTERNAL_REQUEST_COMMANDS.M_UPDATE_MODULE_STATUS,
                                                                    request)


@csrf_exempt
def manage_logout(request):
    return user_auth_controller.getInstance().invoke_trigger(USER_AUTH_COMMANDS.M_LOGOUT, request)


@csrf_exempt
def cms_dashboard(request):
    return dashboard_controller.getInstance().invoke_trigger(DASHBOARD_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def cms_dashboard(request):
    return dashboard_controller.getInstance().invoke_trigger(DASHBOARD_MODEL_CALLBACK.M_INIT, request)


@csrf_exempt
def app_ads(request):
    return render(None, CONSTANTS.S_APP_ADS_PATH, None)


@csrf_exempt
def fetch_anonymous_advert(request):
    return advert_controller.getInstance().invoke_trigger(ADVERT_MODEL_COMMANDS.M_FETCH_ADVERT, request)


def error_page_400(request, exception=None):
    return error_controller.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 400])


def error_page_403(request, exception=None):
    return error_controller.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 403])


def error_page_404(request, exception, template_name='orion/error/error.html'):
    return error_controller.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 404])


def error_page_500(request, exception=None):
    return error_controller.getInstance().invoke_trigger(ERROR_MODEL_CALLBACK.M_INIT, [request, 500])
