from . import views
from django.conf.urls import url
from django.urls import path

app_name = 'NationalityClean'

urlpatterns = [
    path('', views.home, name='home'),
    path('nationality/', views.IndexView.as_view(), name='index'),
    path('individual_nationality_post/', views.PostNationality.as_view(), name='data_post'),
    path('all_nationality_post/', views.PostNationality.as_view(), name='all_data_post')

]