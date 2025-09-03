from django.contrib import admin
from django.db import models

from rates.models import Rate
from core.constants import DEFAULT_EXTRA_FIELD_COUNT


class ProfileRateAssignmentMixin(models.Model):
    rate = models.ForeignKey(
        to=Rate,
        on_delete=models.CASCADE,
        verbose_name='Тариф',
    )
    assigned_at = models.DateTimeField(
        verbose_name='Дата присвоения тарифа',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        verbose_name = 'Присвоение тарифа'
        verbose_name_plural = 'Присвоения тарифов'


class ProfileRateInlineMixin(admin.TabularInline):
    extra = DEFAULT_EXTRA_FIELD_COUNT
    fields = ['rate', 'assigned_at']
    readonly_fields = ['assigned_at']
