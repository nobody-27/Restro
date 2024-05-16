from django.urls import path
from .views import generate_order_number, test

urlpatterns = [
    path("generate-code/", test, name="generate"),
]
