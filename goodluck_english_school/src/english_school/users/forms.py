from django import forms
from django.contrib.auth.forms import UserCreationForm

from profiles.models import TeacherProfile
from profiles.validators import real_age, is_teenager
from core.models import User


class UserRegistrationForm(UserCreationForm):
    birthday_date = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(
            format='%d.%m.%Y',
            attrs={'type': 'date'},
        ),
        validators=[real_age, is_teenager],
    )
    education_level = forms.CharField(
        widget=forms.Select(choices=TeacherProfile.EducationLevel.choices),
        label='Уровень образования',
        required=False,
    )

    consent = forms.BooleanField(
        label='Даю согласие на обработку персональных данных',
        widget=forms.widgets.CheckboxInput(),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthday_date',
            'role',
            'education_level',
            'password1',
            'password2',
            'consent',
        )

    def save(self):
        user = super().save(commit=False)
        user.created_from_user = True

        for field_name in self.fields:
            if field_name in self.cleaned_data:
                setattr(user, field_name, self.cleaned_data.get(field_name))

        user.save()
        return user
