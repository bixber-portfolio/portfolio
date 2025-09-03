from django import forms
from django.forms import widgets

from .models import TeacherProfile, StudentProfile


class ProfileEditFormMixin(forms.ModelForm):

    class Meta:
        widgets = {
            'birthday_date': widgets.SelectDateWidget(years=range(1900, 2008)),
        }


class TeacherProfileEditForm(ProfileEditFormMixin):

    class Meta(ProfileEditFormMixin.Meta):
        model = TeacherProfile
        fields = (
            'bio',
            'education_level',
            'gender_code',
            'birthday_date',
            'image',
            'telegram_username',
        )


class StudentProfileEditForm(ProfileEditFormMixin):

    class Meta(ProfileEditFormMixin.Meta):
        model = StudentProfile
        fields = (
            'bio',
            'gender_code',
            'birthday_date',
            'image',
            'telegram_username',
        )
