from django.urls import path
from .views import (
    receive_network,
    dashboard,
    download_pdf,
    download_excel,
    evil_twin_detection,
    evil_twins_page,

    # Simulation (SINGLE PAGE)
    simulation_dashboard,
    start_simulation,
    stop_simulation,
    log_simulation,
    simulation_sessions,
    session_detail,
    download_session_pdf,
)

urlpatterns = [
    # 🔥 Core
    path('', dashboard),
    path('api/network/', receive_network),

    # 📄 Reports
    path('download/pdf/', download_pdf),
    path('download/excel/', download_excel),

    # 🚨 Evil Twin
    path('api/evil-twin/', evil_twin_detection),
    path('evil-twins/', evil_twins_page),

    # 🎯 Simulation (ONE PAGE ONLY)
    path('simulation/', simulation_dashboard),

    # 🔧 Simulation APIs
    path('api/simulation/start/', start_simulation),
    path('api/simulation/stop/', stop_simulation),
    path('api/simulation/log/', log_simulation),


    path('simulation/sessions/', simulation_sessions, name='simulation_sessions'),
    path('simulation/session/<int:session_id>/',session_detail, name='session_detail'),



    path('simulation/session/<int:session_id>/pdf/', download_session_pdf, name='session_pdf'),
]