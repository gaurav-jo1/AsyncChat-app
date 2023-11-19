from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import ProgrammingLanguages
from .serializers import ProgrammingLanguages_Serializer

from rest_framework.views import APIView


# Create your views here.
# 1. Function Based View
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def languages_list(request):
    if request.method == "GET":
        languages = ProgrammingLanguages.objects.all()
        if languages.exists():
            serializer = ProgrammingLanguages_Serializer(languages, many=True)
            return Response(
                data={
                    "message": "Here is the list of languages.",
                    "languages": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            data={
                "message": "No data available.",
                "languages": None,
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    elif request.method == "POST":
        data = request.data.get("language")

        if data:
            add_language, created = ProgrammingLanguages.objects.get_or_create(
                language_name=data
            )

            if created:
                return Response(
                    data={
                        "message": f"The new language '{data}' is added.",
                        "language": data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(data={"message": f"The language already exist"})

        else:
            return Response(
                {"error": "Please provide a language name."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 2. Class based view
class languages_class_list(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        languages_list = ProgrammingLanguages.objects.all()

        if languages_list:
            serializer = ProgrammingLanguages_Serializer(languages_list, many=True)
            return Response(
                data={
                    "message": "Here is the list of Languages",
                    "languages": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            data={
                "message": "The list is empty",
                "languages": None,
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    def post(self, request):
        language = request.data.get("language")

        if language:
            add_language, created = ProgrammingLanguages.objects.get_or_create(
                language_name=language
            )

            if created:
                return Response(
                    data={
                        "message": f"The new language '{language}' is added.",
                        "language": language,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(data={"message": f"The language already exist"})

        else:
            return Response(
                {"error": "Please provide a language name."},
                status=status.HTTP_400_BAD_REQUEST,
            )
