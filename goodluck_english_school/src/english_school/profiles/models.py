from django.db import models

from rates.models import Rate
from core.models import User, UserProfileBase
from core.constants import EDUCATION_CODE_LENGTH
from .mixins import ProfileRateAssignmentMixin


class TeacherRateAssignment(ProfileRateAssignmentMixin):
    teacher_profile = models.ForeignKey(
        to='TeacherProfile',
        on_delete=models.CASCADE,
        verbose_name='Профиль преподавателя',
    )

    class Meta(ProfileRateAssignmentMixin.Meta):
        db_table = 'teacher_rate_assignment'
        unique_together = ('rate', 'teacher_profile')
        indexes = [
            models.Index(
                fields=['rate'],
                name='teacher_rate_assignment_idx',
            ),
            models.Index(
                fields=['teacher_profile'],
                name='teacher_p_rate_assignment_idx',
            ),
        ]

    def __str__(self):
        return f'{self.rate} для {self.teacher_profile}'


class StudentRateAssignment(ProfileRateAssignmentMixin):
    student_profile = models.ForeignKey(
        to='StudentProfile',
        on_delete=models.CASCADE,
        verbose_name='Профиль преподавателя',
    )

    class Meta(ProfileRateAssignmentMixin.Meta):
        db_table = 'student_rate_assignment'
        unique_together = ('rate', 'student_profile')
        indexes = [
            models.Index(
                fields=['rate'],
                name='student_rate_assignment_idx',
            ),
            models.Index(
                fields=['student_profile'],
                name='student_p_rate_assignment_idx',
            ),
        ]

    def __str__(self):
        return f'{self.rate} для {self.student_profile}'


class TeacherProfile(UserProfileBase):

    class EducationLevel(models.TextChoices):
        BASIC_GENERAL = 'BGE', 'Основное общее образование'
        SECONDARY_GENERAL = 'SGE', 'Среднее общее образование'
        SECONDARY_VOCATIONAL = 'SVE', 'Среднее профессиональное образование'
        HIGHER_BACHELOR = 'HBE', 'Высшее образование (бакалавриат)'
        HIGHER_MASTER = 'HME', 'Высшее образование (магистратура)'
        HIGHER_POSTGRADUATE = 'HPE', 'Высшее образование (аспирантура)'
        __empty__ = 'Выберите Ваш уровень образования:'

    user = models.OneToOneField(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        limit_choices_to={'role': User.Role.TEACHER},
    )
    rates = models.ManyToManyField(
        to=Rate,
        through=TeacherRateAssignment,
        through_fields=('teacher_profile', 'rate'),
        verbose_name='Тарифы',
        blank=True,
        related_name='teacher_rate_profiles',
    )
    education_level = models.CharField(
        verbose_name='Уровень образования',
        max_length=EDUCATION_CODE_LENGTH,
        choices=EducationLevel.choices,
    )

    class Meta(UserProfileBase.Meta):
        db_table = 'teacher_profile'
        verbose_name = 'Профиль преподавателя'
        verbose_name_plural = 'Профили преподавателей'
        indexes = [
            models.Index(
                fields=['telegram_username'],
                name='telegram_username_idx',
            ),
        ]

    def __str__(self):
        return f'Профиль преподавателя {self.user.get_first_last_name()}'


class StudentProfile(UserProfileBase):

    user = models.OneToOneField(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': User.Role.STUDENT},
    )
    rates = models.ManyToManyField(
        to=Rate,
        through=StudentRateAssignment,
        through_fields=('student_profile', 'rate'),
        verbose_name='Тарифы',
        blank=True,
        related_name='student_rate_profiles',
    )

    class Meta(UserProfileBase.Meta):
        db_table = 'student_profile'
        verbose_name = 'Профиль студента'
        verbose_name_plural = 'Профили студентов'
        indexes = [
            models.Index(
                fields=['telegram_username'],
                name='telegram_username_index',
            ),
        ]

    def __str__(self):
        return f'Профиль студента {self.user.get_first_last_name()}'
