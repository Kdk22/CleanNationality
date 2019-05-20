from . import views
from django.conf.urls import url
from django.urls import path

app_name = 'nationality_clean'

urlpatterns = [
    path('', views.home, name='home'),
    path('nationality/', views.IndexView.as_view(), name='index'),
    path('nationality_post/<int:pk>/', views.PostNationality.as_view(), name='data_post'),
    path('all_nationality_post/', views.PostAllNationality.as_view(), name='all_data_post')

]