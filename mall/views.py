from django.shortcuts import render
from django.http import HttpResponse #Temporary
# Create your views here.

def index(request):
    return HttpResponse("Hello World!")