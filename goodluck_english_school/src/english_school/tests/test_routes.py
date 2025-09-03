from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
def test_home_availability_for_anonymous_user(client):
    url = reverse('homepage')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_redirect_not_auth_user_from_lesson_schedule_page(client):
    login_url = reverse('users:login')
    url = reverse('lessons:schedule_lesson')
    response = client.get(url)
    assertRedirects(response, login_url)


@pytest.mark.django_db
def test_lesson_schedule_page_availability_for_student(student_client):
    url = reverse('lessons:schedule_lesson')
    response = student_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('student_user_not_owner_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('student_user_owner_client'), HTTPStatus.NOT_FOUND)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('profiles:profile_detail',),
)
@pytest.mark.django_db
def test_profile_page_availability_for_different_users(
        parametrized_client, name, student_user_owner, expected_status
):
    url = reverse(name, kwargs={'username': student_user_owner.username})
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
