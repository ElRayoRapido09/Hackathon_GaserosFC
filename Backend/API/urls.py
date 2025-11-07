from django.urls import path
from . import views

urlpatterns = [
    path('flights/', views.get_active_flights, name='active_flights'),
    path('flights/save/', views.get_and_save_flights, name='save_flights'),
    path('snapshots/', views.get_snapshots, name='get_snapshots'),
]