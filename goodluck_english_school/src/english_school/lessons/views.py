from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.signing import Signer, BadSignature

from core.models import User
from profiles.models import TeacherProfile
from .models import Lesson, LessonStatus
from .forms import LessonInitialForm


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonInitialForm
    template_name = 'lessons/lesson_form.html'
    success_url = reverse_lazy('lessons:schedule_lesson')

    def get_request_user(self):
        return self.request.user

    def get_user_role(self):
        return self.get_request_user().role

    def get_user_lessons(self):
        if self.get_user_role() == User.Role.TEACHER:
            return Lesson.objects.filter(
                teacher=self.get_request_user(),
            ).exclude(status='finished')
        return Lesson.objects.filter(
            student=self.get_request_user(),
        ).exclude(status='finished')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_request_user()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.get_user_role()
        context['lessons'] = self.get_user_lessons().order_by('started_from')
        if self.get_user_role() == User.Role.STUDENT:
            context['lessons_history_card_title'] = 'Запланированные занятия'
        elif self.get_user_role() == User.Role.TEACHER:
            context['lessons_history_card_title'] = 'Предстоящие занятия'
        return context

    def dispatch(self, request, *args, **kwargs):
        if not self.get_request_user().is_authenticated:
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)


class LessonListView(ListView):
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    context_object_name = 'lessons'

    def get_lessons_status(self):
        return self.kwargs['status']

    def get_request_user(self):
        return self.request.user

    def get_user_role(self):
        return self.get_request_user().role

    def get_user_lessons(self):
        if self.get_user_role() == User.Role.TEACHER:
            return Lesson.objects.filter(
                teacher=self.get_request_user(),
            )
        return Lesson.objects.filter(
            student=self.get_request_user(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.get_user_role()
        if self.get_user_role() == User.Role.STUDENT:
            context['card_title'] = 'Запланированные занятия'
        elif self.get_user_role() == User.Role.TEACHER:
            context['card_title'] = 'Предстоящие занятия'
        return context

    def get_queryset(self):
        if self.get_lessons_status() == 'planned':
            return self.get_user_lessons().exclude(status='finished')
        elif self.get_lessons_status() == 'finished':
            return self.get_user_lessons().exclude(
                status__in=('pending', 'teacher_found')
            )


def get_teacher_users_by_rate(request):
    selected_rate = request.GET.get('rate')
    teacher_users = TeacherProfile.objects.filter(
        rates=selected_rate,
    ).values(
        'user__id',
        'user__first_name',
        'user__last_name',
    )
    return JsonResponse(list(teacher_users), safe=False)


def lesson_confirm(request, signed_lesson_id):
    signer = Signer()
    try:
        lesson_id = signer.unsign(signed_lesson_id)
        lesson = Lesson.objects.get(pk=lesson_id)
        lesson.status = LessonStatus.objects.get(code='teacher_found')
        lesson.save()
        return render(request, 'lessons/lesson_confirm_done.html')
    except BadSignature:
        return render(request, 'lessons/lesson_confirm_failed.html')


def lesson_finished_approve(request, signed_lesson_id):
    signer = Signer()
    try:
        lesson_id = signer.unsign(signed_lesson_id)
        lesson = Lesson.objects.get(pk=lesson_id)
        lesson.status = LessonStatus.objects.get(code='finished')
        lesson.save()
        return render(request, 'lessons/lesson_affirm_done.html')
    except BadSignature:
        return render(request, 'lessons/lesson_affirm_failed.html')
