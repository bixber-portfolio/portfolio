from django.contrib import admin


from .models import Rate


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'title',
        'lesson_cost',
    )
    fieldsets = (
        ('Идентификатор и название', {'fields': (
            'code',
            'title',
        )}),
        ('Условия', {'fields': (
            'lesson_cost',
        )}),
        ('Оформление', {'fields': (
            'theme_image',
        )}),
        ('Дополнительная информация', {'fields': (
            'description',
        )}),
    )
