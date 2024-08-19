from django.contrib import admin
from django.urls import path
from trustly import views

urlpatterns = [

    # redirections
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('privacy/', views.privacy, name='privacy'),
    path('report/', views.report, name='report'),
    path('reportus/', views.report, name='report'),
    path('notice/', views.notice, name='notice'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('secretkey/', views.secretkey, name='secretkey'),
    path('directory/', views.directory, name='directory'),
    path('search/', views.search, name='search'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('cms/login/', views.cms_login, name='cms'),
    path('cms/', views.cms_login, name='cms'),
    path('cms/manage_status/', views.manage_status, name='manage_status'),
    path('cms/manage_search', views.manage_search, name='manage_search'),
    path('cms/dashboard/', views.cms_dashboard, name='dashboard'),
    path('user_index/', views.user_index, name='user_index'),
    path('update_crawl_url/', views.update_crawl_url, name='update_crawl_url'),
    path('.well-known/pki-validation/3841DB2F1945B5BFB45731D4350D205C.txt', views.ssl_validation, name='ssl_validation'),
    path('.well-known/bridges.txt', views.bridges, name='bridges'),
    path('crawl_index/', views.crawl_index, name='crawl_index'),
    path('restricted/', views.restricted_static, name='restricted'),
    path('download/', views.download, name='download'),
    path('downloads/', views.download, name='download'),
    path('download_iframe/', views.download_iframe, name='download_iframe'),
    path('crawl_url/', views.crawl_url, name='crawl_url'),
    path('crawl_url_complete/', views.crawl_url_complete, name='crawl_url_complete'),

    # hotlinks
    path('cms/manage_authentication', views.manage_authentication, name='manage_search'),
    path('cms/logout', views.manage_logout, name='cms_logout'),
    path('update_status/', views.update_status, name='manage_search'),

]

handler400 = views.error_page_400
handler403 = views.error_page_403
handler404 = views.error_page_404
handler500 = views.error_page_500
