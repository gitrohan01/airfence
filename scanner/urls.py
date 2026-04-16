from django.urls import path
from .views import (
    receive_network,
    dashboard,
    download_pdf,
    download_excel,
    evil_twin_detection,
    evil_twins_page,   # 🔥 ADD 
    start_simulation,
    log_simulation,
    simulation_dashboard
    
)

urlpatterns = [
    path('api/network/', receive_network),
    path('', dashboard),

    path('download/pdf/', download_pdf),
    path('download/excel/', download_excel),

    # 🔥 API (already working)
    path('api/evil-twin/', evil_twin_detection),

    # 🔥 NEW UI PAGE
    path('evil-twins/', evil_twins_page),


    path('api/simulation/start/', start_simulation),
    
    path('api/simulation/log/', log_simulation),

    path('simulation/', simulation_dashboard),
]