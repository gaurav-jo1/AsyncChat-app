from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser

from .models import ProgrammingLanguages
from .serializers import ProgrammingLanguages_Serializer


# Create your views here.
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
                "languages": [],
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
