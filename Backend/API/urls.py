from django.urls import path
from . import views

urlpatterns = [
    path('flights/', views.get_active_flights, name='active_flights'),
]