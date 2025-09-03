from datetime import date

import pytest
from django.test.client import Client

from profiles.models import StudentProfile


@pytest.fixture
def student_user(django_user_model):
    return django_user_model.objects.create(
        username='sadfgdfsaf',
        email='bixbertsaf@gmail.com',
        role=django_user_model.Role.STUDENT,
    )


@pytest.fixture
def student_client(student_user):
    client = Client()
    client.force_login(student_user)
    return client


@pytest.fixture
def student_user_owner(django_user_model):
    return django_user_model.objects.create(
        username='user_name',
        email='bixbero@gmail.com',
        role=django_user_model.Role.STUDENT,
    )


@pytest.fixture
def student_user_not_owner(django_user_model):
    return django_user_model.objects.create(
        username='suser_names',
        email='bixberw@gmail.com',
        role=django_user_model.Role.STUDENT,
    )


@pytest.fixture
def owner_client(owner):
    client = Client()
    client.force_login(owner)
    return client


@pytest.fixture
def not_owner_client(not_owner):
    client = Client()
    client.force_login(not_owner)
    return client


@pytest.fixture
def student_user_owner_client(student_user_owner):
    client = Client()
    client.force_login(student_user_owner)
    return client


@pytest.fixture
def student_user_not_owner_client(student_user_not_owner):
    client = Client()
    client.force_login(student_user_not_owner)
    return client


@pytest.fixture
def student_profile(student_user):
    student_profile = StudentProfile.objects.create(
        user=student_user,
        birthday_date=date(2004, 5, 3),
    )
    return student_profile


@pytest.fixture
def student_profile1(student_user_owner):
    student_profile = StudentProfile.objects.create(
        user=student_user_owner,
        birthday_date=date(2004, 5, 3),
    )
    return student_profile


@pytest.fixture
def student_profile2(student_user_not_owner):
    student_profile = StudentProfile.objects.create(
        user=student_user_not_owner,
        birthday_date=date(2004, 5, 3),
    )
    return student_profile
