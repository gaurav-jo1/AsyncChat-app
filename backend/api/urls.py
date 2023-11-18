from django.urls import path
from . import views

urlpatterns = [
    path('<str:new_language>/', views.ProgrammingLanguages, name="Getting or Addiing Languages"),
]