"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APIClient


def pytest_itemcollected(item):
    """ Add access to database for each test"""
    item.add_marker("django_db")


@pytest.fixture()
def client():
    client = APIClient()
    client.force_login(
        User.objects.get_or_create(username="testuser", is_staff=True)[0]
    )
    return client


@pytest.fixture(autouse=True)
def _media_root(settings, tmpdir_factory) -> None:
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp("media", numbered=True)


@pytest.fixture(autouse=True)
def _password_hashers(settings) -> None:
    """Forces django to use fast password hashers for tests."""
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ]


@pytest.fixture(autouse=True)
def _auth_backends(settings) -> None:
    """Deactivates security backend from Axes app."""
    settings.AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)


@pytest.fixture()
def main_heading() -> str:
    """An example fixture containing some html fragment."""
    return "<h1>wemake-django-template</h1>"
