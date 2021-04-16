from django.urls import path

from .views import generate_code

urlpatterns = [
    path("", generate_code, name="generate_code")
]
