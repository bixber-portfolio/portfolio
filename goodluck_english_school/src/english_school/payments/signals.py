from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib import messages
from decimal import Decimal

from lessons.models import Lesson, LessonStatus
from orders.models import Order, OrderStatus
from core.models import User
from core.mappings import WALLET_BALANCE_MAPPING
from .models import Wallet, WalletTransaction


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created and getattr(instance, 'created_from_user', None):
        start_balance = WALLET_BALANCE_MAPPING.get(instance.role)
        Wallet.objects.create(user=instance, balance=start_balance)


@receiver(pre_save, sender=Order)
def create_wallet_transaction(sender, instance, **kwargs):
    if instance.status and instance.status.code == 'ready':
        wallet = Wallet.objects.get(user=instance.user)
        order_amount = sum(
            service.price for service in instance.services.all()
        )
        wallet_transaction = WalletTransaction.objects.create(
            wallet=wallet,
            amount=order_amount,
            type=WalletTransaction.Type.PAYMENT,
        )
        wallet_transaction.perform_transaction()
        instance.status = OrderStatus.objects.get(code='paid')
        instance.save()
        messages.success(instance.request, 'Заказ успешно оплачен')


@receiver(post_save, sender=Lesson)
def pay_lesson_bill(sender, instance, **kwargs):
    if instance.status == LessonStatus.objects.get(code='finished'):
        student_wallet = instance.student.wallet_from_user
        teacher_wallet = instance.teacher.wallet_from_user
        lesson_price = instance.rate.lesson_cost
        teacher_reward = lesson_price * Decimal(0.6)
        student_wallet_transaction = WalletTransaction.objects.create(
            wallet=student_wallet,
            amount=lesson_price,
            type=WalletTransaction.Type.OUTCOME,
        )
        teacher_wallet_transaction = WalletTransaction.objects.create(
            wallet=teacher_wallet,
            amount=teacher_reward,
            type=WalletTransaction.Type.INCOME,
        )
        student_wallet_transaction.perform_transaction()
        teacher_wallet_transaction.perform_transaction()
