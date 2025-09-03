from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from profiles.validators import is_teenager, real_age
from core.validators import starts_with_uppercase
from core.constants import (
    SMALL_FIELD_LENGTH,
    SMALL_DESCRIPTION_FIELD_LENGTH,
    GENDER_CODE_LENGTH,
    MAX_TELEGRAM_USERNAME_LENGTH,
    PRIMARY_KEY_CODE_LENGHT,
)

User = get_user_model()


class UserProfileBase(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Мужской'
        FEMALE = 'F', 'Женский'
        __empty__ = 'Выберите Ваш пол:'

    gender_code = models.CharField(
        verbose_name='Пол',
        max_length=GENDER_CODE_LENGTH,
        null=True,
        blank=True,
        choices=Gender.choices,
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True,
        null=True,
        help_text='Напишите что-нибудь о себе',
    )
    birthday_date = models.DateField(
        verbose_name='Дата рождения',
        help_text='Укажите дату Вашего рождения',
        validators=[real_age, is_teenager],
    )
    image = models.ImageField(
        verbose_name='Фотография',
        upload_to='profiles/images/',
        width_field='image_width',
        height_field='image_height',
        blank=True,
        null=True,
    )
    image_width = models.PositiveSmallIntegerField(
        verbose_name='Ширина изображения профиля',
        null=True,
        editable=False,
    )
    image_height = models.PositiveSmallIntegerField(
        verbose_name='Длина изображения профиля',
        null=True,
        editable=False,
    )
    telegram_username = models.CharField(
        verbose_name='Никнейм в Telegram',
        max_length=MAX_TELEGRAM_USERNAME_LENGTH,
        null=True,
        blank=True,
        unique=True,
        help_text='Укажите ваш никнейм в мессенджере Telegram без символа "@"',
    )

    class Meta:
        abstract = True
        ordering = ('-birthday_date',)

    def get_absolute_url(self):
        return reverse(
            'profiles:profile_detail',
            kwargs={'username': self.user.username},
        )


class SlugBasedModel(models.Model):
    code = models.SlugField(
        verbose_name='Идентификатор',
        max_length=PRIMARY_KEY_CODE_LENGHT,
        primary_key=True,
        help_text='Уникальный идентификатор из латинских символов',
    )

    class Meta:
        abstract = True


class GenericLabelBase(SlugBasedModel):

    title = models.CharField(
        verbose_name='Название',
        max_length=SMALL_FIELD_LENGTH,
        unique=True,
        validators=[starts_with_uppercase],
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
        unique=True,
        max_length=SMALL_DESCRIPTION_FIELD_LENGTH,
        validators=[starts_with_uppercase],
    )

    class Meta:
        abstract = True
        ordering = ('title',)
        indexes = [
            models.Index(
                fields=('title',),
                name='%(class)s_title_idx',
                ),
        ]

    def __str__(self):
        return self.title
