from ipware import get_client_ip
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in


@receiver(user_logged_in)
def update_user_login_ip(sender, request, user, **kwargs):
    ip_address, _ = get_client_ip(request)
    user.last_login_ip = ip_address
    user.save()
