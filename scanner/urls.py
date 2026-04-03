from django.urls import path
from .views import receive_network, dashboard, download_pdf, download_excel

urlpatterns = [
    path('api/network/', receive_network),
    path('', dashboard),

    path('download/pdf/', download_pdf),
    path('download/excel/', download_excel),
]

