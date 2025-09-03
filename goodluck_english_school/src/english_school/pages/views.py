from http import HTTPStatus

from django.views.generic import TemplateView
from django.shortcuts import render


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class ContactPage(TemplateView):
    template_name = 'pages/contacts.html'


class StudentsRulePage(TemplateView):
    template_name = 'pages/useful_links/for_students.html'


class TeacherRulePage(TemplateView):
    template_name = 'pages/useful_links/for_teachers.html'


class PrivacyPolicyPage(TemplateView):
    template_name = 'pages/useful_links/privacy_policy.html'


def page_not_found(request, exception):
    template_name = 'error_pages/404.html'
    return render(request, template_name, status=HTTPStatus.NOT_FOUND)


def permission_denied(request, reason=''):
    template_name = 'error_pages/403.html'
    return render(request, template_name, status=HTTPStatus.FORBIDDEN)


def server_error(request):
    template_name = 'error_pages/500.html'
    return render(
        request,
        template_name,
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )
