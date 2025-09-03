from django.contrib import admin
from django.forms import forms
from django.forms.models import BaseInlineFormSet

from .models import Service, ServiceType, ServicePreference, Preference


class PreferenceInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        num_forms = 0
        for form in self.forms:
            if form.cleaned_data:
                num_forms += 1
        if num_forms > 3:
            raise forms.ValidationError(
                'Нельзя добавить более трех предпочтений',
            )


class ServicePreferenceInline(admin.TabularInline):
    extra = 0
    formset = PreferenceInlineFormSet
    fields = ['preference']
    verbose_name = 'Присвоение предпочтения для выбора услуги клиентом'
    verbose_name_plural = 'Присвоения предпочтений для выбора услуги клиентом'
    model = ServicePreference


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    inlines = (ServicePreferenceInline,)
    list_display = (
        'id',
        'title',
        'price',
        'type',
        'rate',
        'created_at',
    )
    list_filter = (
        'type',
        'rate',
        'created_at',
    )
    fieldsets = (
        ('Основная информация', {'fields': (
            'title',
            'description',
            'image',
            'type',
        )}),
        ('Ценообразующие данные', {'fields': (
            'rate',
        )}),
        ('Цена', {'fields': (
            'price',
        )}),
    )
    add_fieldsets = fieldsets


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
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


@admin.register(Preference)
class ServicePreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
    )
    fieldsets = (
        ('Текстовые данные', {'fields': (
            'text',
        )}),
    )
    add_fieldsets = fieldsets
