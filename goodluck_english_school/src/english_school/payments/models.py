import uuid

from django.db import models
from django.core.validators import MinValueValidator

from core.models import GenericLabelBase, User
from core.constants import DEFAULT_DECIMAL_PLACES
from .constants import (
    MAX_WALLET_BALANCE_DIGITS,
    MINIMUM_WALLET_BALANCE,
    MAX_TRANSACTION_TYPE_FIELD_LENGTH,
)


# class PaymentStatus(GenericLabelBase):

#     class Meta(GenericLabelBase.Meta):
#         db_table = 'payment_status'
#         managed = False


class WalletStatus(GenericLabelBase):

    class Meta(GenericLabelBase.Meta):
        verbose_name = 'Статус электронного кошелька'
        verbose_name_plural = 'Статусы электронного кошелька'
        db_table = 'wallet_status'

    def __str__(self):
        return self.title


class Wallet(models.Model):
    id = models.UUIDField(
        primary_key=True,
        verbose_name='Уникальный генерируемый идентификатор',
        default=uuid.uuid4,
        editable=False,
    )
    user = models.OneToOneField(
        to=User,
        verbose_name='Владелец',
        related_name='wallet_from_user',
        on_delete=models.CASCADE,
    )
    balance = models.DecimalField(
        verbose_name='Баланс',
        max_digits=MAX_WALLET_BALANCE_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
        validators=[MinValueValidator(MINIMUM_WALLET_BALANCE)],
    )
    status = models.ForeignKey(
        to=WalletStatus,
        db_column='status_code',
        verbose_name='Статус',
        related_name='wallets_from_status',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Электронный кошелёк'
        verbose_name_plural = 'Электронные кошельки'
        db_table = 'wallet'
        indexes = (
            models.Index(
                fields=('user',),
                name='%(class)s_user_idx',
            ),
            models.Index(
                fields=('status',),
                name='%(class)s_status_idx',
            ),
        )
        ordering = ('-user__date_joined',)

    def __str__(self):
        return f'Электронный кошелёк пользователя {self.user}'


class WalletTransaction(models.Model):

    class Type(models.TextChoices):
        INCOME = 'income', 'Пополнение'
        OUTCOME = 'outcome', 'Списание'
        PAYMENT = 'payment', 'Оплата'
        RESERVING = 'reserving', 'Резервирование'

    wallet = models.ForeignKey(
        to=Wallet,
        verbose_name='Кошелек',
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        verbose_name='Сумма',
        max_digits=MAX_WALLET_BALANCE_DIGITS,
        decimal_places=DEFAULT_DECIMAL_PLACES,
    )
    type = models.CharField(
        verbose_name='Тип',
        choices=Type.choices,
        max_length=MAX_TRANSACTION_TYPE_FIELD_LENGTH,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'Транзакция виртуального счета'
        verbose_name_plural = 'Транзакции виртуального счета'
        db_table = 'wallet_transaction'
        indexes = (
            models.Index(
                fields=('type',),
                name='%(class)s_type_idx',
            ),
            models.Index(
                fields=('wallet',),
                name='%(class)s_wallet_idx',
            ),
        )
        ordering = ('-created_at',)

    def __str__(self):
        return (
            f'Транзакция для кошелька {self.wallet}: '
            f'{self.get_type_display()} на сумму {self.amount}'
        )

    def perform_transaction(self):
        if self.type in (WalletTransaction.Type.INCOME, WalletTransaction.Type.PAYMENT):
            self.wallet.balance += self.amount  # Начисление денег
        elif self.type == WalletTransaction.Type.OUTCOME:
            self.wallet.balance -= self.amount  # Списание денег
        # Добавьте другие операции в соответствии с типами транзакций

        self.wallet.save()
