
from django.urls import path
from . import views

urlpatterns = [
    path("model/", views.index,name = "index"),
    path("base/",views.first, name = "base"),
]