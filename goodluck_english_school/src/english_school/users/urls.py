from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('registration/', views.RegistrationCreateView.as_view(), name='registration'),
    path('registration/done/', views.DoneRegistrationTemplateView.as_view(), name='registration_done'),
    path('email-confirmation-sent/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', views.UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', views.EmailConfirmedView.as_view(), name='email_confirmation_done'),
    path('confirm-email-failed/', views.EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
]
