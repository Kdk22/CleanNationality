from . import views
from django.conf.urls import url
from django.urls import path

app_name = 'NationalityClean'

urlpatterns = [
    path('', views.home, name='home'),
    path('nationality/', views.IndexView.as_view(), name='index')

]