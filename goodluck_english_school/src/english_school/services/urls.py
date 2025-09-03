from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('all', views.ServicesList.as_view(), name='services_list'),
    path('<service_id>/detail', views.ServiceDetail.as_view(), name='service_detail'),
]