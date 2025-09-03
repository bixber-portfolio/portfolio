from django.utils import timezone

from django.db import models

from core.models import GenericLabelBase, User
from rates.models import Rate
from .validators import validate_time_interval


class LessonStatus(GenericLabelBase):

    class Meta(GenericLabelBase.Meta):
        db_table = 'lesson_status'
        verbose_name = 'Статус занятия'
        verbose_name_plural = 'Статусы занятия'


class Lesson(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True,
        help_text='Дата и время создания занятия',
    )
    started_from = models.DateTimeField(
        verbose_name='Время начала',
        help_text='Дата и время начала занятия',
        validators=[validate_time_interval],
    )
    finished_to = models.DateTimeField(
        verbose_name='Время окончания',
        help_text=(
            'Дата и время конца занятия.\n'
            'Оставьте пустым, если занятие длится не более 1 часа'
        ),
        validators=[validate_time_interval],
        blank=True,
    )
    status = models.ForeignKey(
        to=LessonStatus,
        db_column='status_code',
        verbose_name='Статус',
        related_name='lessons_from_status',
        on_delete=models.SET_NULL,
        null=True,
    )
    teacher = models.ForeignKey(
        to=User,
        verbose_name='Преподаватель',
        limit_choices_to={'role': User.Role.TEACHER},
        on_delete=models.PROTECT,
        related_name='lessons_with_teacher',
    )
    student = models.ForeignKey(
        to=User,
        verbose_name='Студент',
        limit_choices_to={'role': User.Role.STUDENT},
        on_delete=models.PROTECT,
        related_name='lessons_with_student',
    )
    rate = models.ForeignKey(
        to=Rate,
        verbose_name='Тариф',
        on_delete=models.SET_NULL,
        null=True,
        related_name='lessons_from_rate',
    )

    class Meta:
        db_table = 'lesson'
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        indexes = (
            models.Index(
                fields=('started_from',),
                name='%(class)s_start_idx',
            ),
            models.Index(
                fields=('finished_to',),
                name='%(class)s_finish_idx',
            ),
            models.Index(
                fields=('teacher',),
                name='%(class)s_teacher_idx',
            ),
            models.Index(
                fields=('student',),
                name='%(class)s_student_idx',
            ),
            models.Index(
                fields=('rate',),
                name='%(class)s_rate_idx',
            ),
            models.Index(
                fields=('status',),
                name='%(class)s_status_idx',
            ),
        )
        ordering = ('-started_from',)

    def __str__(self):
        return (
            f'Занятие {self.started_from.strftime("%d.%m.%Y %H:%M")} - '
            f'{self.finished_to.strftime("%H:%M")}'
        )

    def get_default_finished_to(self):
        return (
            timezone.localtime(self.started_from)
            + timezone.timedelta(hours=1)
        )

    def save(self, *args, **kwargs):
        if not self.pk and not self.finished_to:
            self.finished_to = self.get_default_finished_to()
        super(Lesson, self).save(*args, **kwargs)
