from datetime import date

from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from core.models import User
from core.constants import DAYS_IN_YEAR
from lessons.models import Lesson, LessonStatus
from .models import TeacherProfile, StudentProfile
from .forms import TeacherProfileEditForm, StudentProfileEditForm


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profiles/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self):
        username = self.kwargs.get(self.slug_url_kwarg)
        user = get_object_or_404(User, username=username)
        return user

    def get_profile(self):
        user = self.get_object()
        if user.role == User.Role.TEACHER:
            return get_object_or_404(TeacherProfile, user=user)
        return get_object_or_404(StudentProfile, user=user)

    def get_user_age(self):
        return ((date.today() - self.get_profile().birthday_date).days
                // DAYS_IN_YEAR)

    def get_user_lessons(self):
        if self.get_object().role == User.Role.TEACHER:
            is_exists_lessons = Lesson.objects.filter(
                teacher=self.get_object(),
            ).exists()
            if is_exists_lessons:
                return Lesson.objects.filter(
                    teacher=self.get_object(),
                    status=LessonStatus.objects.get(code='finished')
                )
        is_exists_lessons = Lesson.objects.filter(
            student=self.get_object(),
        ).exists()
        if is_exists_lessons:
            return Lesson.objects.filter(
                student=self.get_object(),
                status=LessonStatus.objects.get(code='finished')
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = {
            'user': self.get_object(),
            'profile': self.get_profile(),
            'user_age': self.get_user_age(),
            'lessons': self.get_user_lessons(),
        }
        context['lessons'] = self.get_user_lessons()
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object() and not request.user.is_superuser:
            return HttpResponseForbidden(
                'У вас недостаточно прав для просмотра данного профиля'
            )
        return super().dispatch(request, *args, **kwargs)


class ProfileUpdateView(UpdateView):
    template_name = 'profiles/profile_update.html'
    slug_url_kwarg = 'username'

    def get_user(self):
        username = self.kwargs.get(self.slug_url_kwarg)
        user = get_object_or_404(User, username=username)
        return user

    def get_queryset(self):
        if TeacherProfile.objects.filter(user=self.get_user()).exists():
            return TeacherProfile.objects.all()
        return StudentProfile.objects.all()

    def get_object(self):
        return self.get_queryset().get(user=self.get_user())

    def get_form_class(self):
        if isinstance(self.get_object(), TeacherProfile):
            return TeacherProfileEditForm
        return StudentProfileEditForm

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_user():
            return HttpResponseForbidden(
                'У вас недостаточно прав для редактирования данного профиля'
            )
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'profiles/profile_update.html'
    slug_url_kwarg = 'username'
    fields = (
        'email',
        'last_name',
        'first_name',
        'patronymic',
        'phone_number',
        'is_news_sub',
    )
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit_user'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object():
            return HttpResponseForbidden(
                'У вас недостаточно прав для редактирования данного профиля'
            )
        return super().dispatch(request, *args, **kwargs)
