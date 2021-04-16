from django.urls import path

from .views import create_code

urlpatterns = [
    path("", create_code, name="create_code")
]
