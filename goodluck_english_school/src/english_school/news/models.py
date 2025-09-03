from django.db import models

from core.models import User
from core.validators import starts_with_uppercase


class News(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Черновик'
        PUBLISHED = 'PUB', 'Опубликовано'

    title = models.CharField(
        verbose_name='Название',
        max_length=256,
        unique_for_date='created_at',
        help_text='Название новости не более 256 символов',
        validators=(starts_with_uppercase,),
    )
    text = models.TextField(
        verbose_name='Текст',
        unique=True,
        validators=(starts_with_uppercase,),
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='news/images/',
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        limit_choices_to={'is_staff': True, 'is_superuser': True},
        on_delete=models.DO_NOTHING,
        related_name='news_from_author',
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=15,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
        help_text='Дата и время обновления',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        help_text='Дата и время создания',
    )

    class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        unique_together = ('title', 'text')
        indexes = (
            models.Index(
                fields=('-created_at',),
                name='%(class)s_publish_idx',
            ),
        )
        ordering = ('-created_at', 'title')

    def __str__(self):
        return (
            f'Новость от {self.created_at.date().strftime("%d.%m.%Y")} — '
            f'"{self.title[:60]}"'
        )
