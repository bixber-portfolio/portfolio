from django.views.generic import TemplateView
from django.shortcuts import render

from http import HTTPStatus


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    template_name = 'pages/404.html'
    return render(request, template_name, status=HTTPStatus.NOT_FOUND)


def permission_denied(request, reason=''):
    template_name = 'pages/403csrf.html'
    return render(request, template_name, status=HTTPStatus.FORBIDDEN)


def server_error(request):
    template_name = 'pages/500.html'
    return render(
        request,
        template_name,
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
