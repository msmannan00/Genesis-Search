from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Genesis.controllers.view_managers.server_views.block_manager.block_controller import block_controller
from Genesis.controllers.view_managers.server_views.block_manager.block_enums import BLOCK_MODEL_CALLBACK
from Genesis.controllers.view_managers.server_views.maintenance.maintenance_controller import maintenance_controller
from Genesis.controllers.view_managers.server_views.maintenance.maintenance_enums import MAINTENANCE_MODEL_CALLBACK
from Genesis.controllers.view_managers.server_views.secret_key.secret_key_controller import secret_key_controller
from Genesis.controllers.view_managers.server_views.secret_key.secret_key_enums import SECRET_KEY_MODEL_CALLBACK
from Genesis.controllers.view_managers.server_views.user_index_manager.user_index_controller import user_index_controller
from Genesis.controllers.view_managers.server_views.user_index_manager.user_index_enums import USER_INDEX_MODEL_CALLBACK
from Genesis.controllers.view_managers.user_views.directory_manager.directory_controller import directory_controller
from Genesis.controllers.view_managers.user_views.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from Genesis.controllers.view_managers.user_views.hompage_manager.homepage_controller import homepage_controller
from Genesis.controllers.view_managers.user_views.hompage_manager.homepage_enums import HOMEPAGE_MODEL_COMMANDS
from Genesis.controllers.view_managers.user_views.notice_manager.notice_controller import notice_controller
from Genesis.controllers.view_managers.user_views.notice_manager.notice_enums import NOTICE_MODEL_CALLBACK
from Genesis.controllers.view_managers.user_views.policy_manager.policy_controller import policy_controller
from Genesis.controllers.view_managers.user_views.policy_manager.policy_enums import POLICY_MODEL_CALLBACK
from Genesis.controllers.view_managers.user_views.report_manager.report_controller import report_controller
from Genesis.controllers.view_managers.user_views.report_manager.report_enums import REPORT_MODEL_COMMANDS
from Genesis.controllers.view_managers.user_views.search_manager.search_controller import search_controller
from Genesis.controllers.view_managers.user_views.search_manager.search_enums import SEARCH_MODEL_COMMANDS
from Genesis.controllers.view_managers.user_views.sitemap_manager.sitemap_controller import sitemap_controller
from Genesis.controllers.view_managers.user_views.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS


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
def maintenance(request):
    return maintenance_controller.getInstance().invoke_trigger(MAINTENANCE_MODEL_CALLBACK.M_INIT, request)

@csrf_exempt
def block(request):
    return block_controller.getInstance().invoke_trigger(BLOCK_MODEL_CALLBACK.M_INIT, request)
