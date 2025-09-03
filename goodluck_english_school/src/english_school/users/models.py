from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.conf import settings
from users.validators import phone_validator

from core.constants import (
    USER_ERROR_MESSAGES,
    MEDIUM_FIELD_LENGTH,
    BIG_FIELD_LENGTH,
    MAX_PHONE_LENGTH,
    PRIMARY_KEY_CODE_LENGHT,
)
from core.validators import starts_with_uppercase


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username,
                     first_name, last_name, password, **extra_fields):
        """
        Create and save a user with the given username, email,
        full_name, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        if not first_name:
            raise ValueError('The given first name must be set')
        if not last_name:
            raise ValueError('The given last name must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, first_name,
                    last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, username, first_name, last_name, password, **extra_fields,
        )

    def create_superuser(self, email, username, first_name,
                         last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            email, username, first_name, last_name, password, **extra_fields,
        )


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.STUDENT)


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.TEACHER)


class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        STUDENT = 'student', 'Студент'
        TEACHER = 'teacher', 'Преподаватель'
        __empty__ = 'Выберите Вашу роль:'

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name='Логин',
        max_length=MEDIUM_FIELD_LENGTH,
        unique=True,
        help_text=(
            'Обязательное поле. Не более 100 символов. '
            'Можно использовать алфавит латиницы, цифры и символы @/./+/-/'
        ),
        validators=[username_validator],
        error_messages={
            'unique': USER_ERROR_MESSAGES['USERNAME_UNIQUE_ERROR'],
        },
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=BIG_FIELD_LENGTH,
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        error_messages={
            'unique': USER_ERROR_MESSAGES.get('EMAIL_UNIQUE_ERROR'),
        },
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=MAX_PHONE_LENGTH,
        unique=True,
        blank=True,
        null=True,
        validators=[phone_validator],
        error_messages={
            'unique': (USER_ERROR_MESSAGES.get('PHONE_UNIQUE_ERROR')),
        },
        help_text="В формате +7XXXXXXXXXX или 8XXXXXXXXXX",
    )
    last_login_ip = models.GenericIPAddressField(
        verbose_name='IP-адрес клиента',
        protocol='ipv4',
        blank=True,
        null=True,
        help_text='Последний IP-адрес входа в систему',
    )
    last_login = models.DateTimeField(
        verbose_name='Последний вход',
        blank=True,
        null=True,
        help_text='Дата и время последнего входа.',
    )
    role = models.SlugField(
        verbose_name='Роль',
        max_length=PRIMARY_KEY_CODE_LENGHT,
        choices=Role.choices,
        db_index=True,
        help_text='Роль пользователя в системе.',
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MEDIUM_FIELD_LENGTH,
        validators=[starts_with_uppercase],
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=BIG_FIELD_LENGTH,
        null=True,
        blank=True,
        validators=[starts_with_uppercase],
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=MEDIUM_FIELD_LENGTH,
        null=True,
        blank=True,
        help_text='При наличии',
        validators=[starts_with_uppercase],
    )
    is_staff = models.BooleanField(
        verbose_name='Статус персонала',
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True,
    )
    is_news_sub = models.BooleanField(
        verbose_name='Подписка на рассылку',
        default=False,
        help_text=('Указывает, получает ли пользователь '
                   'новостную рассылку на электронную почту.'),
    )
    date_joined = models.DateTimeField(
        verbose_name='Регистрация',
        default=timezone.now,
        help_text='Дата и время регистрации.',
    )

    objects = UserManager()
    students = StudentManager()
    teachers = TeacherManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']
        indexes = [
            models.Index(
                fields=['-date_joined', 'last_login'],
                name='activity_idx',
                ),
        ]

    def __str__(self):
        return f'{self.first_name} [{self.username}] {self.last_name}'

    def set_deleted_value(self):
        return f'[DELETED] {self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse(
            'profiles:profile_detail',
            kwargs={'username': self.username},
        )

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return f'{self.first_name} {self.patronymic}'

    def get_first_last_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def email_user(
        self,
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        **kwargs,
    ):
        send_mail(subject, message, from_email, [self.email], **kwargs)
