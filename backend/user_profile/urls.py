from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Get_Users.as_view(), name="Get_users_list"),
]
