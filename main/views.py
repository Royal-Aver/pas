from django.shortcuts import render

from products.models import Category


def index(request):
    context = {}
    return render(request, "main/index.html", context)


def about(request):
    return render(request, "main/about.html")
