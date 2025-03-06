
from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index,name = "index"),
    path("result",views.get_diopter_result, name = "result"),
    path('',views.User, name = "base"),
]