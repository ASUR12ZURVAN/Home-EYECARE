from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World")

def first(request):
    return render(request,'index.html')

# Create your views here.
