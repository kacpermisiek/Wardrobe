from django.shortcuts import render
from stuff.models import Item


def home(request):
    context = {
        'stuff': Item.objects.all(),
        'title': 'Home page'
    }
    return render(request, 'stuff/home.html', context)


def about(request):
    context = {
        'title': 'About page'
    }
    return render(request, 'stuff/about.html', context)
