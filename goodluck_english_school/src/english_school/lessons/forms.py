from django.utils import timezone
from django import forms
from django.forms import widgets

from core.models import User
from .models import Lesson, LessonStatus


class LessonInitialForm(forms.ModelForm):
    consent = forms.BooleanField(
        label='Даю согласие на обработку персональных данных',
        widget=forms.widgets.CheckboxInput(),
    )

    class Meta:
        model = Lesson
        fields = (
            'rate',
            'teacher',
            'started_from',
            'consent',
        )
        widgets = {
            'started_from': widgets.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'min': timezone.now().strftime('%Y-%m-%dT%H:%M'),
                }
            )
        }
        labels = {
            'rate': 'Выберите тариф',
            'teacher': 'Выберите преподавателя',
            'started_from': 'Дата и удобное время',
        }

    def __init__(self, *args, user=None, request=None, **kwargs):
        self.student = user
        self.request = request
        super(LessonInitialForm, self).__init__(*args, **kwargs)

        if user and user.role == User.Role.STUDENT:
            self.fields['rate'].queryset = user.student_profile.rates.all()

    def clean(self):
        cleaned_data = super().clean()
        if (
            self.student.wallet_from_user.balance
            < cleaned_data['rate'].lesson_cost
        ):
            raise forms.ValidationError(
                'У вас недостаточно средств для выбранного тарифа. '
                'Пополните баланс или выберите другой тариф'
            )
        return cleaned_data

    def save(self, commit=True):
        lesson = super(LessonInitialForm, self).save(commit=False)
        lesson.student = self.student
        lesson.status = LessonStatus.objects.get(code='pending')
        lesson.request = self.request
        if commit:
            lesson.save()
        return lesson
