from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutPage.as_view(), name='about'),
    path('contacts/', views.ContactPage.as_view(), name='contacts'),
    path('student_rules/', views.StudentsRulePage.as_view(), name='student_rules'),
    path('teacher_rules/', views.TeacherRulePage.as_view(), name='teacher_rules'),
    path('privacy_policy/', views.PrivacyPolicyPage.as_view(), name='privacy_policy'),
]