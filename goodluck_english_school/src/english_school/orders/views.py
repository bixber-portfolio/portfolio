from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

from services.models import Service
from .models import Order, OrderService, OrderStatus


class CreateOrderView(FormView, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        try:
            service_id = request.POST.get('service_id')
            order_obj = Order.objects.create(user=request.user)
            service = Service.objects.get(id=service_id)
            OrderService.objects.create(
                order=order_obj, service=service,
            )
            order_obj.status = OrderStatus.objects.get(code='ready')
            order_obj.request = request
            order_obj.save()
            messages.success(request, 'Заказ успешно подготовлен для оплаты')
        except Exception as err:
            messages.error(request, f'Ошибка создания заказа: {err}')
            return redirect('services:service_detail', service_id)

        assigned_rates = [
            service.rate.__str__() for service in order_obj.services.all()
        ]
        assigned_rates_str = ', '.join(assigned_rates)
        messages.info(
            request, f'Вам присвоены новые тарифы: {assigned_rates_str}'
        )

        return redirect('profiles:profile_detail', request.user.username)

    def get_success_url(self):
        return reverse('pages:contacts')
