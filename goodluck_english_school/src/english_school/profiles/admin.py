from django.contrib import admin
from .models import (
    TeacherProfile,
    StudentProfile,
    TeacherRateAssignment,
    StudentRateAssignment,
)

from .mixins import ProfileRateInlineMixin


class TeacherProfileRateInline(ProfileRateInlineMixin):
    verbose_name = 'Присвоение тарифа преподавателю'
    verbose_name_plural = 'Присвоения тарифа преподавателям'
    model = TeacherRateAssignment


class StudentProfileRateInline(ProfileRateInlineMixin):
    verbose_name = 'Присвоение тарифа студенту'
    verbose_name_plural = 'Присвоения тарифа студентам'
    model = StudentRateAssignment


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    inlines = (TeacherProfileRateInline,)
    list_display = (
        'user',
        'birthday_date',
        'education_level',
        'telegram_username',

    )
    list_filter = (
        'education_level',
        'gender_code',
    )
    fieldsets = (
        ('Пользователь', {'fields': (
            'user',
        )}),
        ('Биография', {'fields': (
            'image',
            'bio',
        )}),
        ('Персональная информация', {'fields': (
            'gender_code',
            'birthday_date',
            'education_level',
        )}),
        ('Контакты', {'fields': (
            'telegram_username',
        )}),
    )
    add_fieldsets = fieldsets


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    inlines = (StudentProfileRateInline,)
    list_display = (
        'user',
        'birthday_date',
        'telegram_username',
    )
    list_filter = (
        'gender_code',
    )
    fieldsets = (
        ('Пользователь', {'fields': (
            'user',
        )}),
        ('Биография', {'fields': (
            'image',
            'bio',
        )}),
        ('Персональная информация', {'fields': (
            'gender_code',
            'birthday_date',
        )}),
        ('Контакты', {'fields': (
            'telegram_username',
        )}),
    )
    add_fieldsets = fieldsets
