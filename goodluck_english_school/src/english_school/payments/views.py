from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class ReservationView(View, LoginRequiredMixin):
    pass
