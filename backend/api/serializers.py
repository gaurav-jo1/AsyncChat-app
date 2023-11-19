from rest_framework import serializers

from .models import ProgrammingLanguages

class ProgrammingLanguages_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguages
        fields = '__all__'