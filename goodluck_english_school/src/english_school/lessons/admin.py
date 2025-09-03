from django.contrib import admin

from .models import Lesson, LessonStatus


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = (
        'teacher',
        'student',
        'status',
        'rate',
        'created_at',
    )
    list_filter = (
        'status',
        'rate',
        'started_from',
        'created_at',
    )
    fieldsets = (
        ('Тариф', {'fields': (
            'rate',
        )}),
        ('Участники', {'fields': (
            'student',
            'teacher',
        )}),
        ('Дата и время', {'fields': (
            'started_from',
            'finished_to',
        )}),
        ('Статус', {'fields': (
            'status',
        )}),
    )
    add_fieldsets = (
        ('Тариф', {'fields': (
            'rate',
        )}),
        ('Участники', {'fields': (
            'student',
            'teacher',
        )}),
        ('Дата и время', {'fields': (
            'started_from',
        )}),
        ('Статус', {'fields': (
            'status',
        )}),
    )


@admin.register(LessonStatus)
class LessonStatusAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title',
        'description',
    )
    list_filter = (
        'title',
    )
    fieldsets = (
        ('Идентификатор', {'fields': (
            'code',
        )}),
        ('Уникальное название', {'fields': (
            'title',
        )}),
        ('Описание', {'fields': (
            'description',
        )}),
    )
    add_fieldsets = fieldsets
