from django.urls import path
from . import views

urlpatterns = [
    path('', views.languages_list, name="get_or_add_languages"),
    path('class_add/', views.languages_class_list.as_view(), name="class_get_or_add_languages"),
]
