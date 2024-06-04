# myapp/tests.py
import pytest
from django.contrib.auth.models import User
import pytest
from django.test import RequestFactory
from rest_framework.response import Response
from rest_framework import status
from api.views import languages_list
from rest_framework.test import APIRequestFactory
from api.models import ProgrammingLanguages


# GET
@pytest.mark.django_db
def test_languages_list_get_request():
    languages_arr = ["Python", "JavaScript", "Java", "Rust", "Ruby"]

    for language in languages_arr:
        ProgrammingLanguages.objects.create(
            language_name=language,
        )

    # Create a request instance
    request = RequestFactory().get("/")

    # Call the view function
    response = languages_list(request)

    # Check if response status code is 200
    assert response.status_code == status.HTTP_200_OK


# POST
@pytest.mark.django_db
def test_languages_list_no_content():
    # Create a request instance

    language_name = "Python"
    request = RequestFactory().post("/", {"language": language_name})

    # Call the view function
    response = languages_list(request)

    # Check if response status code is 201
    assert response.status_code == status.HTTP_201_CREATED

    # Check if the language was created in the database
    assert ProgrammingLanguages.objects.filter(language_name=language_name).exists()


from api.views import languages_class_list


@pytest.mark.django_db
def test_languages_class_list_get():
    # Create some languages for testing
    ProgrammingLanguages.objects.create(language_name="Python")
    ProgrammingLanguages.objects.create(language_name="JavaScript")

    # Create a GET request instance
    factory = APIRequestFactory()
    request = factory.get("/class_add/")

    # Call the view function
    response = languages_class_list.as_view()(request)

    # Check if response status code is 200
    assert response.status_code == status.HTTP_200_OK

    # Check if languages are returned in the response
    assert len(response.data["languages"]) == 2


@pytest.mark.django_db
def test_languages_class_list_post_created():
    # Create a POST request instance with a new language
    factory = APIRequestFactory()
    request = factory.post("/class_add/", {"language": "Java"})

    # Call the view function
    response = languages_class_list.as_view()(request)

    # Check if response status code is 201
    assert response.status_code == status.HTTP_201_CREATED

    # Check if the language was created in the database
    assert ProgrammingLanguages.objects.filter(language_name="Java").exists()


@pytest.mark.django_db
def test_languages_class_list_post_exists():
    # Create a language in the database
    ProgrammingLanguages.objects.create(language_name="Java")

    # Create a POST request instance with the existing language name
    factory = APIRequestFactory()
    request = factory.post("/class_add/", {"language": "Java"})

    # Call the view function
    response = languages_class_list.as_view()(request)

    # Check if response status code is 200
    assert response.status_code == status.HTTP_200_OK

    # Check if the message indicates that the language already exists
    assert "language already exist" in response.data["message"]


@pytest.mark.django_db
def test_languages_class_list_post_no_language_provided():
    # Create a POST request instance without providing a language name
    factory = APIRequestFactory()
    request = factory.post("/class_add/")

    # Call the view function
    response = languages_class_list.as_view()(request)

    # Check if response status code is 400
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Check if the error message is present in the response
    assert "Please provide a language name." in response.data["error"]
