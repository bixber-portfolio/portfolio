from datetime import datetime
from django import forms
from django.forms import widgets, ValidationError
from django.utils import timezone

from lessons.models import Lesson
from core.constants import MEDIUM_FIELD_LENGTH
from core.validators import starts_with_uppercase
from notifications.utils import (
    send_first_lesson_info_email_to_student,
    send_first_lesson_request_email_to_teacher,
)


class IntroForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        max_length=MEDIUM_FIELD_LENGTH,
        validators=(starts_with_uppercase,)
    )
    email = forms.EmailField(
        label='Адрес электронной почты',
    )
    convenient_datetime = forms.DateTimeField(
        label='Дата и удобное время',
        widget=widgets.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'min': timezone.now().strftime('%Y-%m-%dT06:00'),
                'max': (timezone.now() + timezone.timedelta(days=90)).strftime(
                    '%Y-%m-%dT22:00'
                ),
            },
        ),
    )
    consent = forms.BooleanField(
        label='Даю согласие на обработку персональных данных',
        widget=forms.widgets.CheckboxInput(),
    )

    def clean_convenient_datetime(self):
        convenient_datetime = self.cleaned_data.get('convenient_datetime')
        if convenient_datetime:
            if (
                convenient_datetime.time()
                < datetime.strptime('06:00', '%H:%M').time()
                or convenient_datetime.time()
                > datetime.strptime('22:00', '%H:%M').time()
            ):
                raise ValidationError(
                    'Время должно быть в диапазоне с 6:00 до 21:00. '
                    'Преподавателям тоже нужен отдых.'
                )
            elif convenient_datetime > (
                timezone.now() + timezone.timedelta(days=90)
            ):
                raise ValidationError(
                    'Планировать заявку более чем на 3 месяца вперед нельзя.'
                )
        return convenient_datetime

    def clean(self):
        cleaned_data = super().clean()
        is_have_lesson = Lesson.objects.filter(
            student__email=cleaned_data['email']
        ).exists()

        if is_have_lesson:
            raise ValidationError(
                'Пользователь с таким email уже зарегистрирован и '
                'воспользовался пробным занятием.\n'
                'Войдите в аккаунт для записи на новое занятие '
                'с преподавателем.',
            )
        return cleaned_data

    def send_emails(self, teacher_user=None):
        send_first_lesson_request_email_to_teacher(
            teacher_user,
            self.cleaned_data,
        )
        send_first_lesson_info_email_to_student(self.cleaned_data)
