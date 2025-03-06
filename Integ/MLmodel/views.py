from django.shortcuts import render
from django.http import HttpResponse
from MLmodel.model import DiopterDataModel


model = DiopterDataModel(r"D:\MY REPO\Home-EYECARE\Integ\MLmodel\diopter_data_combined2.csv")


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
        line_number = request.POST.get("line_number")
        distance_str = request.POST.get("distance")

        if not resolution or not line_number or not distance:
            return render(request, "error.html", {"message": "Missing input values."})

        try:
            line_number = int(line_number)
        except ValueError:
            return render(request, "error.html", {"message": "Invalid line number."})

        if resolution not in PIXEL_SIZES or not (1 <= line_number <= len(PIXEL_SIZES[resolution])):
            return render(request, "error.html", {"message": "Invalid line number or resolution."})

        pixel_size = PIXEL_SIZES[resolution][line_number - 1]

        #this is needed because the numpy needs float or int to work on
        #and currently distance was in string so it was giving error
        #we use a map to solve this

        distance_map = {"25cm":0.25,"3m":3.0}
        distance = distance_map.get(distance_str,None)

        if distance is None:
            return render(request, "error.html",{"message":"Invalid distance value."})


        diopter = model.get_diopter(pixel_size, resolution)


        return render(request, "diopter_result.html", {
            "diopter": diopter,
            "distance": distance, 
            "resolution": resolution
        })
