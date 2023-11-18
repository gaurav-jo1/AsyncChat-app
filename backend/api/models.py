from django.db import models
import uuid


# Create your models here.
class ProgrammingLanguages(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    language_name = models.CharField(max_length=255)

    def __str__(self):
        return self.language_name