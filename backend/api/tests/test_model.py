from django.test import TestCase
from api.models import ProgrammingLanguages

class ProgrammingLanguagesTest(TestCase):
    def setUp(self):
        # Create a sample ProgrammingLanguages object for testing
        programming_languages = [
        "Python",
        "JavaScript",
        "Java",
        "C++",
        "C#",
        "TypeScript",
        "Ruby",
        "Swift",
        "Go",
        "Kotlin",
        "Rust",
        "PHP",
        "HTML",
        "CSS",
        "SQL",
        ]

        for language in programming_languages:
            ProgrammingLanguages.objects.create(language_name=language)

    def test_language_name(self):
        # Retrieve the ProgrammingLanguages object from the database
        python_language = ProgrammingLanguages.objects.get(language_name='Python')
        javascript_language = ProgrammingLanguages.objects.get(language_name='JavaScript')
        html_language = ProgrammingLanguages.objects.get(language_name='HTML')
        kotlin_language = ProgrammingLanguages.objects.get(language_name='Kotlin')

        # Check if the retrieved object matches the one created in the setUp method
        self.assertEqual(python_language.language_name, 'Python')
        self.assertEqual(javascript_language.language_name, 'JavaScript')
        self.assertEqual(html_language.language_name, 'HTML')
        self.assertEqual(kotlin_language.language_name, 'Kotlin')

