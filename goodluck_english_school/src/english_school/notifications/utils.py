from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.models import Site

current_site = Site.objects.get_current().domain


def send_request_email_to_teacher(lesson, confirmation_url):
    subject = 'Подтверждение занятия'
    message = (
        f'Запрос на занятие ожидает вашего подтверждения. '
        f'{lesson.__str__()}\n{lesson.rate}\n'
        f'Ученик: {lesson.student.get_first_last_name()}\n\n'
        f'**Подтвердить занятие: http://{current_site}{confirmation_url}'
        f'\n**Нажимая на ссылку выше, Вы соглашаетесь '
        f'с правилами сервиса и ответственностью за проведение онлайн-занятия.'
    )
    lesson.teacher.email_user(subject, message, fail_silently=False)


def send_affirmation_email_to_teacher(lesson, affirmation_url):
    subject = 'Подтверждение успешного проведения занятия'
    message = (
        f'При успешном проведении занятия, которое Вы подтвердили: '
        f'{lesson.__str__()}\n{lesson.rate}\n'
        f'Ученик: {lesson.student.get_first_last_name()}\n\n'
        f'**Подтвердить успешно проведенное занятие: '
        f'http://{current_site}{affirmation_url}'
        f'\n**Нажимая на ссылку выше, Вы соглашаетесь '
        f'с правилами сервиса и ответственностью за качество '
        f'проведённого онлайн-занятия.'
    )
    lesson.teacher.email_user(subject, message, fail_silently=False)


def send_info_email_to_student(lesson):
    subject = 'Запись на онлайн-занятие'
    message = (
        f'Вы видите это сообщение, потому что недавно оставили запрос '
        f'на сайте http://{current_site} для записи на '
        f'онлайн-{lesson.__str__().lower()} '
        f'по английскому языку с преподавателем '
        f'{lesson.teacher.get_first_last_name()}.'
        f'\n\nЕсли в ответ, не менее, чем за 2 часа до начала '
        f'планируемого занятия, Вам не придет сообщение на почту об '
        f'успешном подтверждении Вашего занятия — преподаватель '
        f'не смог подтвердить Ваше занятие. В таком случае, Вы можете '
        f'попробовать создать заявку ещё раз, выбрав того же или иного '
        f'преподавателя.'
    )
    lesson.student.email_user(subject, message, fail_silently=False)


def send_success_email_to_student(lesson):
    subject = 'Ваше занятие подтверждено'
    teacher_telegram = lesson.teacher.teacher_profile.telegram_username
    if teacher_telegram:
        telegram_link = f'https://t.me/{teacher_telegram}'
        contact_telegram_msg = (
            f'Связаться с преподавателем (Telegram): {telegram_link}\n'
        )
    else:
        contact_telegram_msg = ''
    message = (
        f'Ваше {lesson.__str__()} было успешно подтверждено преподавателем!\n'
        f'Ваш преподаватель: {lesson.teacher.get_first_last_name()}\n\n'
        f'{contact_telegram_msg}'
        f'Связаться с преподавателем (Email): {lesson.teacher.email}'
    )
    lesson.student.email_user(subject, message, fail_silently=False)


def send_reward_email_to_teacher(lesson):
    subject = 'Вознаграждение за проведенное занятие'
    message = (
        f'{lesson.teacher.first_name}, спасибо за '
        f'проведенное {lesson.__str__()}.\n'
        f'Мы уже зачислили вознаграждение на Ваш электронный кошелек.\n\n'
        f'Будем рады видеть Вас снова на '
        f'занятиях с учениками нашей онлайн-школы Goodluck!'
    )
    lesson.teacher.email_user(subject, message, fail_silently=False)


# Trying lessons

def send_first_lesson_info_email_to_student(form_data):
    name = form_data.get('name')
    student_email = form_data.get('email')
    convenient_datetime = form_data.get('convenient_datetime')

    subject = 'Запись на пробное онлайн-занятие (консультация)'
    message = (
        f'Здравствуйте, {name}. Недавно Вы заполнили форму и отправили запрос '
        f'на сайте http://{current_site} для записи на '
        f'пробное (тестовое) онлайн-занятие'
        f'по английскому языку. Наш сервис уже занялся поиском свободного '
        f'преподавателя для оценки Вашего уровня владения языком и '
        f'составления дальнейших рекомендаций по Вашему обучению у нас.'
        f'Как только мы найдем преподавателя — мы попросим его связаться с '
        f'по электронной почте, указанной Вами в форме ({student_email}).'
        f'\n\nЕсли в ответ, не более, чем за 2 часа до времени, указанного '
        f'Вами при заполнении формы ({convenient_datetime}), Вам не придет '
        f'сообщение на почту об '
        f'успешном подтверждении Вашего занятия — мы не смогли подобрать '
        f'преподавателя по Вашей заявке. В таком случае, Вы можете '
        f'попробовать создать заявку ещё раз, выбрав то же или иное '
        f'предпочитаемое время встречи при заполнении формы.'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student_email],
        fail_silently=False,
    )


def send_first_lesson_request_email_to_teacher(teacher_user, form_data):
    name = form_data.get('name')
    email = form_data.get('email')
    convenient_datetime = form_data.get('convenient_datetime')

    subject = 'Запрос на пробное онлайн-занятие'
    message = (
        f'Здравствуйте, {teacher_user.get_first_last_name()}, Вам предложена '
        f'заявка с сайта http://{current_site} на проведение пробного'
        f'занятия от пользователя.\n\nИмя ученика: {name}\nEmail: {email}\n'
        f'Предпочтительное время проведения: {convenient_datetime}\n\n'
        f'Если у Вас имеется возможность принять заявку — свяжитесь с '
        f'пользователем по электронной почте как минимум за 2 часа до '
        f'предпочтительного времени проведения, выбранного пользователем.'
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[teacher_user.email],
        fail_silently=False,
    )
