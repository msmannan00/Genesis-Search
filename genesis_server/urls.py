"""serverListener URL Configuration

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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.privacy, name='privacy'),
    path('', views.report, name='report'),
    path('', views.notice, name='notice'),
    path('', views.sitemap, name='sitemap'),
    path('', views.secretkey, name='secretkey'),
    path('', views.directory, name='directory'),
    path('', views.search, name='search'),
    path('', views.maintenance, name='maintenance'),
    path('', views.user_index, name='user_index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
