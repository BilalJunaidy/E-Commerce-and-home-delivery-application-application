from django.shortcuts import render
from pathlib import Path

# Create your views here.

def store(request):

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    context = {"key": BASE_DIR}
    return render(request, "store/store.html", context)


def cart(request):
    context = {}
    return render(request, "store/cart.html", context)


def checkout(request):
    context = {}
    return render(request, "store/checkout.html", context)