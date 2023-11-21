from django.test import TestCase, Client
from django.urls import reverse

from api.models import ProgrammingLanguages


class Test_Languages(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.my_view_url = reverse("get_or_add_languages")

    def test_language_view_GET(self):
        languages = ["JavaScript", "Kotlin", "Python"]
        for language in languages:
            ProgrammingLanguages.objects.create(language_name=language)

        response = self.client.get(self.my_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["languages"]), len(languages))
        for language in languages:
            self.assertContains(response, language)
        self.assertNotContains(response, "TypeScript")

    def test_get_empty_languages_list(self):
        ProgrammingLanguages.objects.all().delete()

        response = self.client.get(self.my_view_url)

        self.assertEqual(response.status_code, 204)

    def test_language_view_POST(self):
        languages = ["Elixer", "HTML", "CSS"]
        for language in languages:
            response = self.client.post(self.my_view_url, {"language": language})
            self.assertEqual(response.status_code, 201)

        response = self.client.post(self.my_view_url, {"language": ""})
        self.assertEqual(response.status_code, 400)


class Test_Languages_class(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.my_view_url = reverse("class_get_or_add_languages")

    def test_language_view_GET(self):
        languages = ["JavaScript", "Kotlin", "Python"]
        for language in languages:
            ProgrammingLanguages.objects.create(language_name=language)

        response = self.client.get(self.my_view_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["languages"]), len(languages))
        for language in languages:
            self.assertContains(response, language)
        self.assertNotContains(response, "TypeScript")

    def test_get_empty_languages_list(self):
        ProgrammingLanguages.objects.all().delete()

        response = self.client.get(self.my_view_url)

        self.assertEqual(response.status_code, 404)

    def test_language_view_POST(self):
        languages = ["Elixer", "HTML", "CSS"]
        for language in languages:
            response = self.client.post(self.my_view_url, {"language": language})
            self.assertEqual(response.status_code, 201)

        response = self.client.post(self.my_view_url, {"language": ""})
        self.assertEqual(response.status_code, 400)
