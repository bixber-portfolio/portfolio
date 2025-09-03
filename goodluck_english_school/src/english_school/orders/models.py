from django.db import models

from django.core.validators import MinValueValidator
from core.models import GenericLabelBase, User
from services.models import Service

from .constants import MIN_AMOUNT_ORDER_POSITION


class OrderStatus(GenericLabelBase):

    class Meta(GenericLabelBase.Meta):
        db_table = 'order_status'
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    created_at = models.DateTimeField(
        verbose_name='Время создания заказа',
        auto_now_add=True,
        help_text='Дата и время создания заказа',
    )
    user = models.ForeignKey(
        to=User,
        verbose_name='Пользователь',
        related_name='orders',
        on_delete=models.DO_NOTHING,
    )
    services = models.ManyToManyField(
        verbose_name='Услуги',
        to=Service,
        through='OrderService',
        through_fields=('order', 'service'),
        related_name='orders_from_service',
    )
    status = models.ForeignKey(
        to=OrderStatus,
        db_column='status_code',
        verbose_name='Статус',
        related_name='orders_from_status',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'order'
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
        ordering = ('-created_at',)

    def __str__(self):
        return f'Заказ {self.id:04d}'


class OrderService(models.Model):
    order = models.ForeignKey(
        to=Order,
        verbose_name='Заказ',
        related_name='services_from_order',
        on_delete=models.CASCADE,
    )
    service = models.ForeignKey(
        to=Service,
        verbose_name='Услуга',
        related_name='orders_from_services',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(MIN_AMOUNT_ORDER_POSITION),),
        default=MIN_AMOUNT_ORDER_POSITION,
    )

    class Meta:
        db_table = 'order_services'
        verbose_name = 'Услуга заказа'
        verbose_name_plural = 'Услуги заказа'
        unique_together = ('order', 'service')
        indexes = [
            models.Index(
                fields=['order'],
                name='order_services_idx',
            ),
            models.Index(
                fields=['service'],
                name='service_orders_idx',
            ),
        ]
        ordering = ('-service',)

    def __str__(self):
        return f'{self.service} x {self.amount}'
