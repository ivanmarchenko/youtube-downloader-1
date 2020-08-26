"""yd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views

app_name = 'ytd'
urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.yt_download, name='yt_download'),
    path('download_complete/<itag>', views.download_complete, name='download_complete'),
    # path('download_complete/<itag>', views.download_complete, name='download_complete'),
    path('download_2/', views.yt_download2, name='yt_download_2')

]
