from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import value_validator


class User(AbstractUser):

    class Roles(models.TextChoices):
        USER = 'user', _('User')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Administrator')

    unicode_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. Letters, digits and @/./+/-/_ only.'),
        validators=[unicode_validator, value_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        _('about yourself'),
        max_length=450,
        blank=True,
    )
    role = models.CharField(
        _('role'),
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER,
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    @property
    def is_moderator(self):
        return self.role == self.Roles.MODERATOR

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.Roles.ADMIN

    def __str__(self):
        return self.username
