from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name= "index"),
    path('check_connection/', views.check_connection, name = "check_connection"),
]
