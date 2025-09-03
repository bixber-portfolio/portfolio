from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import User
from core.mappings import PROFILE_MAPPING


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if (
        created
        and getattr(instance, 'created_from_user', None)
        and instance.is_active
    ):
        profile_data = {
            'birthday_date': getattr(instance, 'birthday_date', None),
        }
        if instance.education_level:
            profile_data['education_level'] = instance.education_level

        profile_model = PROFILE_MAPPING['models'].get(instance.role)
        if profile_model:
            profile_model.objects.create(user=instance, **profile_data)
