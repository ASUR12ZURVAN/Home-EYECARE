from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World")

def first(request):
    return render(request,'index.html')

def User(request):
    username = request.GET.get('username')
    print(username)
    return render(request,'user.html',{'name':username})



# Create your views here.
