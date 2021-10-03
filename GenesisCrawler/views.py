from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from GenesisCrawler.controllers.directoryManager.DirectoryController import DirectoryController
from GenesisCrawler.controllers.directoryManager.DirectoryControllerEnums import DirectoryModelCommands
from GenesisCrawler.controllers.hompageManager.HomepageController import HomepageController
from GenesisCrawler.controllers.hompageManager.HomepageEnums import HomepageModelCommands
from GenesisCrawler.controllers.noticeManager.NoticeController import NoticeController
from GenesisCrawler.controllers.noticeManager.NoticeControllerEnums import NoticeModelCommands
from GenesisCrawler.controllers.reportManager.ReportController import ReportController
from GenesisCrawler.controllers.reportManager.ReportControllerEnums import ReportModelCommands
from GenesisCrawler.controllers.searchManager.SearchController import SearchController
from GenesisCrawler.controllers.searchManager.SearchControllerEnums import SearchModelCommands
from GenesisCrawler.controllers.sitemapManager.sitemapController import SitemapController
from GenesisCrawler.controllers.sitemapManager.sitemapControllerEnums import SitemapModelCommands


def index(request):
    return HomepageController.getInstance().invoke_trigger(HomepageModelCommands.M_INIT)


@csrf_exempt
def command(request):
    return render(request, 'GenesisCrawler/homepage/index.html', )

@csrf_exempt
def privacy(request):
    return render(request, 'GenesisCrawler/privacy/privacy.html', )

@csrf_exempt
def report(request):
    return ReportController.getInstance().invoke_trigger(ReportModelCommands.M_INIT, request)

@csrf_exempt
def notice(request):
    return NoticeController.getInstance().invoke_trigger(NoticeModelCommands.M_INIT, request)

@csrf_exempt
def sitemap(request):
    return SitemapController.getInstance().invoke_trigger(SitemapModelCommands.M_INIT, request)

@csrf_exempt
def secretkey(request):
    return render(request, 'GenesisCrawler/secretkey/secretkey.html', )

@csrf_exempt
def directory(request):
    return DirectoryController.getInstance().invoke_trigger(DirectoryModelCommands.M_INIT, request)

@csrf_exempt
def search(request):
    return SearchController.getInstance().invoke_trigger(SearchModelCommands.M_INIT, request)
