from django.contrib import admin

from .models import Order, OrderService, OrderStatus
from core.constants import DEFAULT_EXTRA_FIELD_COUNT


class OrderServiceInlineMixin(admin.TabularInline):
    extra = DEFAULT_EXTRA_FIELD_COUNT
    fields = ['service', 'amount']


class OrderServiceInline(OrderServiceInlineMixin):
    verbose_name = 'Присвоение тарифа преподавателю'
    verbose_name_plural = 'Присвоения тарифа преподавателям'
    model = OrderService


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderServiceInline,)
    readonly_fields = ('created_at',)
    list_display = (
        'user',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
    )
    fieldsets = (
        ('Пользователь', {'fields': (
            'user',
        )}),
        ('Статус', {'fields': (
            'status',
        )}),
    )
    add_fieldsets = (
        ('Пользователь', {'fields': (
            'user',
        )}),
        ('Статус', {'fields': (
            'status',
        )}),
    )


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
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
