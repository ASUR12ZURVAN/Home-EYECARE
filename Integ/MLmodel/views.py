import os
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from MLmodel.model import DiopterDataModel

# Load the model dynamically using BASE_DIR
csv_path = os.path.join(settings.BASE_DIR, "MLmodel", "diopter_data_combined2.csv")
model = DiopterDataModel(csv_path)

PIXEL_SIZES = {
    "hd": [322, 299, 276, 252, 229, 207, 184, 161, 138, 116, 92, 69, 46, 29, 1],
    "2k": [437, 406, 375, 344, 312, 281, 250, 218, 187, 156, 125, 94, 62, 39, 2],
    "4k": [642, 598, 553, 509, 464, 420, 375, 331, 286, 242, 197, 148, 98, 62, 3]
}

def index(request):
    return render(request, 'index.html')  

def about(request):
    return render(request, 'about.html')

def User(request):  
    if request.method == "POST":  
        resolution = request.POST.get("resolution")

        if resolution in ["hd", "2k", "4k"]:
            return render(request, f"{resolution}.html", {"resolution": resolution})  

    return render(request, "index.html")


def get_diopter_result(request):
    if request.method == "POST":
        resolution = request.POST.get("resolution")
        line_number = request.POST.get("line_number")
        distance_str = request.POST.get("distance")

        if not resolution or not line_number or not distance_str:
            return render(request, "error.html", {"message": "Missing input values."})

        try:
            line_number = int(line_number)  # Convert to integer
        except ValueError:
            return render(request, "error.html", {"message": "Invalid line number."})

        if resolution not in PIXEL_SIZES:
            return render(request, "error.html", {"message": "Invalid resolution."})

        if not (0 <= line_number < len(PIXEL_SIZES[resolution])):  
            return render(request, "error.html", {"message": "Invalid Line Number."})

        try:
            pixel_size = float(PIXEL_SIZES[resolution][line_number])
        except IndexError:
            return render(request, "error.html", {"message": "Line number exceeded the possible value."})

        # Convert distance string to numeric value
        distance_map = {"25cm": 0.25, "3m": 3.0}
        distance = distance_map.get(distance_str)

        if distance is None:
            return render(request, "error.html", {"message": "Invalid distance value."})

        try:
            diopter = model.get_diopter(pixel_size)  # Ensure inputs are numbers
        except Exception as e:
            return render(request, "error.html", {"message": f"Model Error: {str(e)}"})

        return render(request, "diopter_result.html", {
            "diopter": diopter,
            "distance": distance, 
            "resolution": resolution
        })
