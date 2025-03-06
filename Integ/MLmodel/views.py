from django.shortcuts import render
from django.http import HttpResponse
from MLmodel.model import DiopterDataModel

model = DiopterDataModel("D:\MY REPO\Home-EYECARE\Integ\MLmodel\diopter_data_combined2.csv")

PIXEL_SIZES = {
    "hd": [322, 299, 276, 252, 229, 207, 184, 161, 138, 116, 92, 69, 46, 29, 1],
    "2k": [437, 406, 375, 344, 312, 281, 250, 218, 187, 156, 125, 94, 62, 39, 2],
    "4k": [642, 598, 553, 509, 464, 420, 375, 331, 286, 242, 197, 148, 98, 62, 3]
}

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

def get_diopter_result(request):

    if request.method == "POST":
        resolution = request.POST.get("resolution")
        line_number = int(request.POST.get("line_number"))
        distance = request.POST.get("distance")

    if resolution not in PIXEL_SIZES or not (1 <= line_number <= len(PIXEL_SIZES[resolution])):
        return render(request,"error.html",{"message":"invalid line number or resolution."})

    pixel_size = PIXEL_SIZES[resolution][line_number-1]

    diopter = model.get_diopter(pixel_size,resolution)

    return render(request, "diopter_result.html",{
        "diopter":diopter,
        "disrance":distance,
        "resolution":resolution
    })

    return render(request,"index.html")

