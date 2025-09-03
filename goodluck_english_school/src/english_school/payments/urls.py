from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('reservation/', views.ReservationView.as_view(), name='reservation'),
]