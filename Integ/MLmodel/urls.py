
from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index,name = "index"),
    path("",views.first, name = "base"),
    path('user',views.User,name = "user"),
]