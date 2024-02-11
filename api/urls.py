from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllData, name='getAllData'),
    path('<int:index>/', views.getSpecificData, name='getSpecificData'),
]