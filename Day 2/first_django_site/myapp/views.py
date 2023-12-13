from django.shortcuts import render
from django.http import HttpResponse


def welcome(request):
    return HttpResponse("This is how to customize Welcome page into plain boring one.")


def hello_world(request):
    return HttpResponse("Hello World!")

