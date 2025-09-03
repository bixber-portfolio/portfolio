import random
from datetime import datetime as dt

from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone

from core.models import User
from news.models import News
from orders.models import OrderService
from services.models import Service
from django.db.models import Sum
from .forms import IntroForm


class HomePage(SuccessMessageMixin, FormView):
    template_name = 'english_school/main.html'
    form_class = IntroForm
    success_url = reverse_lazy('homepage')
    success_message = (
        'Ваш запрос успешно отправлен! '
        'Мы также направили Вам краткую инструкцию на указанную Вами '
        'электронную почту'
    )

    def form_valid(self, form):
        if form.is_valid():
            form.send_emails(
                self.get_teacher_user_for_request(
                    form.cleaned_data.get('convenient_datetime'),
                )
            )
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_resent_news'] = News.objects.all()[:3]

        orders_from_student = OrderService.objects.filter(
            order__user__student_profile__birthday_date__gte=dt(2004, 1, 1)
        )
        services_from_student = orders_from_student.values(
            'service'
        ).annotate(
            count=Sum('amount')
        ).order_by('-count').first()
        if services_from_student is not None:
            services_from_student = services_from_student.get('service')
            student_top_service = Service.objects.get(id=services_from_student)
            context['student_top_choice'] = student_top_service
            context['adult_top_choice'] = student_top_service
        return context

    def get_teacher_user_for_request(self, convenient_datetime):
        two_hours_before = convenient_datetime - timezone.timedelta(hours=2)
        two_hours_after = convenient_datetime + timezone.timedelta(hours=2)

        has_lesson_in_range = User.teachers.filter(
            lessons_with_teacher__started_from__range=(
                two_hours_before, two_hours_after
            ),
            lessons_with_teacher__finished_to__range=(
                two_hours_before, two_hours_after
            )
        ).exists()

        time_within_range = (
            convenient_datetime.hour >= 6 and convenient_datetime.hour < 22
        )

        if not has_lesson_in_range and time_within_range:
            return User.teachers.first()
        return random.choice(User.teachers.all())
