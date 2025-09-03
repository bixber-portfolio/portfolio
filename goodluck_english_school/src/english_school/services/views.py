from django.views.generic import ListView, DetailView

from .models import Service


class ServicesList(ListView):
    model = Service
    template_name = 'services/all_services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['common_services'] = Service.objects.filter(
            type='common'
        ).order_by('price')
        context['subscription_services'] = Service.objects.filter(
            type='subscription'
        ).order_by('price')
        return context


class ServiceDetail(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    pk_url_kwarg = 'service_id'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_random_services'] = Service.objects.all(
        ).select_related(
            'rate',
            'type',
            ).exclude(
                id=context['obj'].id
                ).order_by('?')[:3]
        return context
