from django.views.generic import CreateView, View, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.contrib.sites.models import Site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import redirect
from django.contrib.auth import login

from core.models import User
from core.mixins import UserIsNotAuthenticated
from .forms import UserRegistrationForm


class RegistrationCreateView(UserIsNotAuthenticated, CreateView):
    """
    View for the user registration and profile.

    The user profile is created automatically.
    """
    template_name = 'registration/registration_form.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:registration_done')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy(
            'users:confirm_email', kwargs={'uidb64': uid, 'token': token}
        )
        current_site = Site.objects.get_current().domain
        user.email_user(
            'Подтвердите свой электронный адрес',
            (f'Пожалуйста, перейдите по следующей ссылке, '
             f'чтобы подтвердить свой адрес электронной почты: '
             f'http://{current_site}{activation_url}'),
            fail_silently=False,
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if (user is not None
           and default_token_generator.check_token(user, token)):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmation_done')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'registration/email_confirmation_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class DoneRegistrationTemplateView(TemplateView):
    template_name = 'registration/registration_done.html'


# noqa: Small fix the urlpaths...
views.PasswordResetConfirmView.success_url = reverse_lazy(
    'users:password_reset_complete',
)
views.PasswordResetView.success_url = reverse_lazy('users:password_reset_done')
views.PasswordChangeView.success_url = reverse_lazy(
    'users:password_change_done',
)
