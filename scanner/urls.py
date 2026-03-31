from django.urls import path
from .views import receive_network

urlpatterns = [
    path('api/network/', receive_network),
]