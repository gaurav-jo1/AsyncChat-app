from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ProgrammingLanguages

# Create your views here.
@api_view(["GET", "POST"])
def languages_list(request, new_language=None):
    if request.method == "GET":
        languages = ProgrammingLanguages.objects.all()

        if languages:
            return Response(
                data={
                    "message": "Here is the list of languages.",
                    "languages": languages,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            data={
                "message": "No data available.",
                "languages": [],
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    elif request.method == "POST":
        if new_language:
            instance, created = ProgrammingLanguages.objects.get_or_create(
                language_name=new_language
            )

            if created:
                return Response(
                    data={
                        "message": f"The new language '{new_language}' is added.",
                        "language": instance,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                data={
                    "message": f"The language '{new_language}' already exists.",
                    "language": instance,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Please provide a language name."},
                status=status.HTTP_400_BAD_REQUEST,
            )
