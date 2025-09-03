from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator

from core.models import SlugBasedModel
from core.constants import (
    DEFAULT_DECIMAL_PLACES,
    MEDIUM_DESCRIPTION_FIELD_LENGTH,
    SMALL_FIELD_LENGTH,
)
from .validators import svg_size_validator, svg_file_size_validator
from .constants import (
    MAX_PRICE_DIGITS,
    REQUIRED_WIDTH_PX,
    REQUIRED_HEIGTH_PX,
    MIN_LESSON_COST_RUB,
    FILE_EXTENSION_STR,
)


class Rate(SlugBasedModel):
    title = models.CharField(
        verbose_name='Название',
        max_length=SMALL_FIELD_LENGTH,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=MEDIUM_DESCRIPTION_FIELD_LENGTH,
        null=True,
        blank=True,
    )
    lesson_cost = models.DecimalField(
        verbose_name='Стоимость занятия',
        max_digits=MAX_PRICE_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        validators=[MinValueValidator(MIN_LESSON_COST_RUB)],
        help_text='Стоимость одного занятия в рамках тарифа',
    )
    theme_image = models.FileField(
        verbose_name='Стилевая тема',
        upload_to=f'rates/themes/{FILE_EXTENSION_STR.lower()}s/',
        validators=[
            FileExtensionValidator(allowed_extensions=[
                FILE_EXTENSION_STR.lower(),
            ]),
            svg_size_validator,
            svg_file_size_validator,
        ],
        help_text=(
            f'Стилевое изображение тарифа в формате '
            f'{FILE_EXTENSION_STR.upper()} с размером '
            f'{REQUIRED_WIDTH_PX} на {REQUIRED_HEIGTH_PX} пикселей'
        ),
    )

    class Meta:
        db_table = 'rate'
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ['lesson_cost']
        indexes = [
            models.Index(
                fields=['code'],
                name='rate_code_idx',
                ),
        ]

    def __str__(self):
        return f'Тариф «{self.title}»'
