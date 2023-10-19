from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()


def generate_confirmation_code(user):
    return default_token_generator.make_token(user)


def send_email(user, confirmation_code):
    user.email_user(
        subject='Email Verification Request',
        message=(f'{user.username}, your verification code: '
                 f'{confirmation_code}'),
        from_email=settings.AUTH_EMAIL,
        fail_silently=False,
    )


def create_user(serializer, is_signup=False):
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            **serializer.validated_data,
        )
    except IntegrityError:
        return Response(
            {'error': 'This login or email is already exists'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if is_signup:
        confirmation_code = generate_confirmation_code(user)
        user.confirmation_code = confirmation_code
        if user.is_active:
            send_email(user, confirmation_code)
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )
        user.is_active = False
        user.save()
        send_email(user, confirmation_code)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    user.save()
    return Response(
        serializer.validated_data,
        status=status.HTTP_201_CREATED,
    )
