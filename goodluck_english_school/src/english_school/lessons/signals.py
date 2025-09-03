from django.utils import timezone as tz
from django.core.signing import Signer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib import messages

from lessons.models import Lesson, LessonStatus
from notifications.utils import (
    send_request_email_to_teacher,
    send_success_email_to_student,
    send_info_email_to_student,
    send_affirmation_email_to_teacher,
    send_reward_email_to_teacher,
)


@receiver(post_save, sender=Lesson)
def handle_lesson_status(sender, instance, created, **kwargs):
    if created and instance.status == LessonStatus.objects.get(code='pending'):
        signer = Signer()
        signed_lesson_id = signer.sign(str(instance.id))
        confirmation_url = reverse(
            'lessons:lesson_confirmation',
            kwargs={'signed_lesson_id': signed_lesson_id},
        )
        if getattr(instance, 'request', None):
            messages.success(
                request=instance.request,
                message=(
                    'Заявка на запись отправлена! '
                    'Проверьте электронную почту, указанную при регистрации'
                ),
            )
        send_request_email_to_teacher(instance, confirmation_url)
        send_info_email_to_student(instance)

    if (
        instance.status == LessonStatus.objects.get(code='teacher_found')
        and instance.started_from - tz.now() > tz.timedelta(hours=2)
    ):
        send_success_email_to_student(instance)

    elif (
        instance.status == LessonStatus.objects.get(code='teacher_found')
        and instance.finished_to <= tz.now()
    ):
        affirmation_url = reverse(
            'lessons:lesson_affirmation',
            kwargs={'signed_lesson_id': signed_lesson_id},
        )
        send_affirmation_email_to_teacher(instance, affirmation_url)

    elif (instance.status == LessonStatus.objects.get(code='finished')):
        send_reward_email_to_teacher(instance)
