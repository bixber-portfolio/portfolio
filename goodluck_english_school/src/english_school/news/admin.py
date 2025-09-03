from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title', 'text')
    date_hierarchy = ('created_at')
    list_display = (
        'title',
        'text',
        'author',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'author',
        'updated_at',
        'created_at',
    )
    fieldsets = (
        ('Контент', {'fields': (
            'title',
            'text',
            'image',
        )}),
        ('Автор', {'fields': (
            'author',
        )}),
        ('Статус', {'fields': (
            'status',
        )}),
    )
    add_fieldsets = fieldsets
