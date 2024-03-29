"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from polls import views

urlpatterns = [
    url(r'^$',views.default),
    
    # main urls
    url(r'^Login.html',views.Login),
    
    url(r'^UiHomepage.html',views.UiHomepage),
    url(r'^imageToMusic.html',views.imageToMusic),
    url(r'^searchByKeywords.html',views.searchByKeywords),
    url(r'^searchByGeoLocation.html',views.searchByGeoLocation),
    url(r'^filterSongs.html',views.filterSongs),
    url(r'^musicExpert.html',views.musicExpert),
    url(r'^PersonalQueries.html', views.PersonalQueries),

    # services
    url(r'^SignIn*',views.SignInfunc),
    url(r'^LoginUser*',views.LoginUserfunc),
    url(r'^Generic',views.generic),
    
    
    
]
