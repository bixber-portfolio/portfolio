from django.urls import path
from . import views

app_name = 'lessons'

urlpatterns = [
    path('schedule/', views.LessonCreateView.as_view(), name='schedule_lesson'),
    path('get_teacher_users/', views.get_teacher_users_by_rate, name='get_teacher_users'),
    path('confirm_lesson/<str:signed_lesson_id>/', views.lesson_confirm, name='lesson_confirmation'),
    path('approve_lesson/<str:signed_lesson_id>/', views.lesson_finished_approve, name='lesson_affirmation'),
    path('<slug:status>/all/', views.LessonListView.as_view(), name='lesson_list'),
]