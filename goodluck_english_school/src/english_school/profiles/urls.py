from django.urls import path

from . import views

app_name = 'profiles'


urlpatterns = [
    path('<slug:username>/profile/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('<slug:username>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('<slug:username>/profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]