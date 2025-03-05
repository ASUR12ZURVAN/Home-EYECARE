from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')  

def User(request):  
    if request.method == "POST":  
        resolution = request.POST.get("resolution")

        if resolution == "hd":
            return render(request, "hd.html")
        elif resolution == "2k":
            return render(request, "2k.html")
        elif resolution == "4k":
            return render(request, "4k.html")  

    return render(request, "index.html") 
