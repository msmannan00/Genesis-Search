from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from genesis.controllers.view_managers.block_manager.block_controller import block_controller
from genesis.controllers.view_managers.block_manager.block_enums import BLOCK_MODEL_CALLBACK
from genesis.controllers.view_managers.directory_manager.directory_controller import directory_controller
from genesis.controllers.view_managers.directory_manager.directory_enums import DIRECTORY_MODEL_COMMANDS
from genesis.controllers.view_managers.hompage_manager.homepage_controller import homepage_controller
from genesis.controllers.view_managers.hompage_manager.homepage_enums import HOMEPAGE_MODEL_COMMANDS
from genesis.controllers.view_managers.notice_manager.notice_controller import notice_controller
from genesis.controllers.view_managers.notice_manager.notice_enums import NOTICE_MODEL_CALLBACK
from genesis.controllers.view_managers.report_manager.report_controller import report_controller
from genesis.controllers.view_managers.report_manager.report_enums import REPORT_MODEL_COMMANDS
from genesis.controllers.view_managers.search_manager.search_controller import search_controller
from genesis.controllers.view_managers.search_manager.search_enums import SEARCH_MODEL_COMMANDS
from genesis.controllers.view_managers.sitemap_manager.sitemap_controller import sitemap_controller
from genesis.controllers.view_managers.sitemap_manager.sitemap_enums import SITEMAP_MODEL_COMMANDS


def index(request):
    return homepage_controller.getInstance().invoke_trigger(HOMEPAGE_MODEL_COMMANDS.M_INIT, request)


@csrf_exempt
def command(request):
    return render(request, 'genesis/homepage/index.html', )

@csrf_exempt
def privacy(request):
    return render(request, 'genesis/privacy/privacy.html', )

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
    return render(request, 'genesis/secretkey/secretkey.html', )

@csrf_exempt
def directory(request):
    return directory_controller.getInstance().invoke_trigger(DIRECTORY_MODEL_COMMANDS.M_INIT, request)

@csrf_exempt
def block(request):
    return block_controller.getInstance().invoke_trigger(BLOCK_MODEL_CALLBACK.M_INIT, request)

@csrf_exempt
def search(request):
    return search_controller.getInstance().invoke_trigger(SEARCH_MODEL_COMMANDS.M_INIT, request)
