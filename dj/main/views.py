from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
from django.utils.translation import template


def index(request):

    return render(request, 'main/index.html')