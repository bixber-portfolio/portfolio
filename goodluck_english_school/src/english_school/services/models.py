from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError

from rates.models import Rate
from core.validators import starts_with_uppercase
from core.models import GenericLabelBase
from core.constants import (
    MEDIUM_DESCRIPTION_FIELD_LENGTH,
    DEFAULT_DECIMAL_PLACES
)
from .constants import (
    GENERATE_ID_FIELD_LENGTH,
    TITLE_FIELD_LENGTH,
    MAX_PRICE_DIGITS,
    REQUIRED_WIDTH_PX,
    REQUIRED_HEIGTH_PX,
    FILE_EXTENSIONS_STR,
)
from .validators import image_file_size_validator, image_size_validator


class ServiceType(GenericLabelBase):

    class Meta(GenericLabelBase.Meta):
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'
        db_table = 'service_type'

    def __str__(self):
        return self.title


class Preference(models.Model):
    text = models.CharField(
        max_length=256,
        verbose_name='Текст',
        unique=True,
    )

    class Meta:
        db_table = 'preference'
        verbose_name = 'Предпочтение выбора'
        verbose_name_plural = 'Предпочтения выбора'
        ordering = ('-id',)

    def __str__(self):
        return self.text


class ServicePreference(models.Model):
    service = models.ForeignKey(
        to='Service',
        verbose_name='Услуга',
        on_delete=models.CASCADE,
        related_name='preferences_with_service'
    )
    preference = models.ForeignKey(
        to=Preference,
        verbose_name='Предпочтение выбора',
        on_delete=models.CASCADE,
        null=True,
        related_name='services_with_preference',
    )

    class Meta:
        db_table = 'service_preferences'
        verbose_name = 'Предпочтение выбора услуги'
        verbose_name_plural = 'Предпочтения выбора услуг'
        unique_together = ('service', 'preference')
        indexes = [
            models.Index(
                fields=['service'],
                name='service_preferences_idx',
            ),
            models.Index(
                fields=['preference'],
                name='preference_services_idx',
            ),
        ]
        ordering = ('-service', 'preference')

    def __str__(self):
        return f'Предпочтение для {self.service}'


class Service(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=GENERATE_ID_FIELD_LENGTH,
        verbose_name='Уникальный генерируемый идентификатор',
        editable=False,
        validators=[starts_with_uppercase],
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=TITLE_FIELD_LENGTH,
        unique_for_date='created_at',
        validators=[starts_with_uppercase],
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=MEDIUM_DESCRIPTION_FIELD_LENGTH,
        unique=True,
        validators=[starts_with_uppercase],
    )
    price = models.DecimalField(
        verbose_name='Стоимость услуги',
        max_digits=MAX_PRICE_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        validators=[MinValueValidator(0)],
    )
    type = models.ForeignKey(
        to=ServiceType,
        db_column='type_code',
        verbose_name='Тип',
        related_name='services_from_type',
        on_delete=models.SET_NULL,
        null=True,
    )
    preferences = models.ManyToManyField(
        to=Preference,
        through=ServicePreference,
        through_fields=('service', 'preference'),
        verbose_name='Предпочтения выбора услуги',
        related_name='services_from_preference',
        help_text=('Не более трёх предпочтений '
                   'для выбора данной услуги клиентом'),
        blank=True,
    )
    rate = models.ForeignKey(
        to=Rate,
        on_delete=models.SET_NULL,
        verbose_name='Тариф',
        blank=True,
        null=True,
        related_name='services_from_rate',
    )
    image = models.FileField(
        verbose_name='Изображение',
        upload_to='services/images/',
        validators=[
            FileExtensionValidator(allowed_extensions=[
                *FILE_EXTENSIONS_STR,
            ]),
            image_size_validator,
            image_file_size_validator,
        ],
        help_text=(
            f'Изображение услуги в одном из допустимых форматов '
            f'{tuple(map(str.upper, FILE_EXTENSIONS_STR))} с размером '
            f'{REQUIRED_WIDTH_PX} на {REQUIRED_HEIGTH_PX} пикселей'
        ),
    )
    created_at = models.DateField(
        verbose_name='Дата создания',
        auto_now=True,
        help_text='Необходимо для ограничения дубликата услуги в один день',
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        db_table = 'service'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'price'],
                name='unique_%(class)s_with_price',
            ),
            models.UniqueConstraint(
                fields=['title', 'image'],
                name='unique_%(class)s_with_image',
            ),
        ]
        indexes = (
            models.Index(
                fields=('title',),
                name='%(class)s_title_idx',
            ),
            models.Index(
                fields=('price',),
                name='%(class)s_price_idx',
            ),
        )
        ordering = ('title', 'price')

    def __str__(self):
        return f'{self.title} — {self.rate}'

    def clean(self):
        super().clean()
        if len(self.description) <= len(self.title):
            raise ValidationError(
                {'description': ('Минимальная длина описания '
                                 'должна быть больше длины названия')}
            )
        if self.preferences.count() > 3:
            raise ValidationError(
                'Количество предпочтений для выбора не может быть более трех',
            )

    def save(self, *args, **kwargs):
        if not self.id:
            last_obj_id = Service.objects.filter(
                type=self.type
            ).order_by('-id').first()
            if last_obj_id:
                count = int(last_obj_id.id.split('-')[-1])
                self.id = f'{self.type.title[0]}-{count+1:03d}'
            else:
                count = 0
                self.id = f'{self.type.title[0]}-{count+1:03d}'
        super(Service, self).save(*args, **kwargs)
