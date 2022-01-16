"""Settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from genesis_server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('command/', views.command),
    path('privacy/', views.privacy),
    path('report/', views.report),
    path('notice/', views.notice),
    path('sitemap/', views.sitemap),
    path('search/', views.search),
    path('secretkey/', views.secretkey),
    path('directory/', views.directory),
    path('maintenance/', views.maintenance),
    path('user_index/', views.user_index),
    path('', views.index),
]
