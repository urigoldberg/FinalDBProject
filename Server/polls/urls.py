from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mock', views.mock, name='mock'),
    path('mockHTML', views.mockHTML, name='mockHTML')
]
