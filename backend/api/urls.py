from django.urls import path
from . import views

urlpatterns = [
    path('', views.languages_list, name="get_or_add_languages"),
]
