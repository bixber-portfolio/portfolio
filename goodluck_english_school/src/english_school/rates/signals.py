from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import Order


@receiver(pre_save, sender=Order)
def assign_profile_rates(sender, instance, **kwargs):
    if instance.status and instance.status.code == 'paid':
        student_profile = instance.user.student_profile
        paid_services = instance.services.all()
        assignee_rates = [service.rate for service in paid_services]
        student_profile.rates.set(assignee_rates)
        student_profile.save()
