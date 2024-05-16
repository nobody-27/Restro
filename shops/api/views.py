from django.shortcuts import render, HttpResponse
from shops.utils import generate_order_number


# Create your views here.


def test(request):
    return HttpResponse("done")
