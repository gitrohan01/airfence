from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import json

from .models import (
    NetworkObservation,
    AccessPoint,
    SimulationResult,
    SimulationSession
)
from .services.processor import process_network
from .utils.report_generator import generate_pdf, generate_excel


# =========================================================
# 🔥 NETWORK API
# =========================================================
@csrf_exempt
def receive_network(request):
    if request.method == "POST":
        data = json.loads(request.body)
        result = process_network(data)
        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request"}, status=400)


# =========================================================
# 🛡️ DASHBOARD
# =========================================================
def dashboard(request):
    query = request.GET.get('q')
    filter_type = request.GET.get('filter')

    latest_ids = (
        NetworkObservation.objects
        .values('ssid')
        .annotate(latest_id=Max('id'))
        .values_list('latest_id', flat=True)
    )

    networks = NetworkObservation.objects.filter(id__in=latest_ids)

    if query:
        networks = networks.filter(ssid__icontains=query)

    if filter_type:
        networks = networks.filter(classification=filter_type)

    networks = networks.order_by('trust_score')

    secure_count = networks.filter(classification="Secure").count()
    risky_count = networks.filter(classification="Risky").count()
    critical_count = networks.filter(classification="Critical").count()

    alert = critical_count > 0

    return render(request, 'scanner/dashboard.html', {
        'networks': networks,
        'secure_count': secure_count,
        'risky_count': risky_count,
        'critical_count': critical_count,
        'alert': alert
    })


# =========================================================
# 📄 REPORT DOWNLOADS
# =========================================================
def download_pdf(request):
    data = NetworkObservation.objects.all()[:50]
    file_path = "report.pdf"
    generate_pdf(file_path, data)
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


def download_excel(request):
    data = NetworkObservation.objects.all()[:50]
    file_path = "report.xlsx"
    generate_excel(file_path, data)
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


# =========================================================
# 🚨 EVIL TWIN DETECTION
# =========================================================
def evil_twins_page(request):
    results = []

    ssids = AccessPoint.objects.values_list('ssid', flat=True).distinct()

    for ssid in ssids:
        aps = AccessPoint.objects.filter(ssid=ssid)

        if aps.count() > 1:
            results.append({
                "ssid": ssid,
                "count": aps.count(),
                "status": "⚠️ Possible Evil Twin"
            })

    return render(request, 'scanner/evil_twins.html', {"results": results})


def evil_twin_detection(request):
    suspicious = []

    ssids = AccessPoint.objects.values_list('ssid', flat=True).distinct()

    for ssid in ssids:
        aps = AccessPoint.objects.filter(ssid=ssid)

        if aps.count() > 1:
            suspicious.append({
                "ssid": ssid,
                "count": aps.count(),
                "message": "Possible Evil Twin detected"
            })

    return JsonResponse({"evil_twins": suspicious})


# =========================================================
# 🎯 SIMULATION MODULE
# =========================================================

# 🔹 Start Simulation
@csrf_exempt
def start_simulation(request):
    if request.method == "POST":
        data = json.loads(request.body)

        name = data.get("name")
        if not name:
            return JsonResponse({"error": "Session name required"}, status=400)

        session = SimulationSession.objects.create(name=name)

        return JsonResponse({
            "status": "started",
            "session_id": session.id,
            "session_name": session.name
        })

    return JsonResponse({"error": "Use POST request"}, status=400)


# 🔹 Stop Simulation
@csrf_exempt
def stop_simulation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        session_id = data.get("session_id")

        try:
            session = SimulationSession.objects.get(id=session_id)
            session.status = "stopped"
            session.save()

            return JsonResponse({"status": "stopped"})
        except SimulationSession.DoesNotExist:
            return JsonResponse({"error": "Session not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)


# 🔹 Log Simulation Activity
@csrf_exempt
def log_simulation(request):
    if request.method == "POST":
        data = json.loads(request.body)

        session_id = data.get("session_id")
        device_id = data.get("device_id")
        action = data.get("action")

        try:
            session = SimulationSession.objects.get(id=session_id)
        except SimulationSession.DoesNotExist:
            return JsonResponse({"error": "Invalid session"}, status=404)

        # 🔥 Risk Logic
        if action == "connected":
            risk = "High"
        elif action == "completed":
            risk = "Medium"
        else:
            risk = "Low"

        SimulationResult.objects.create(
            session=session,
            device_id=device_id,
            action=action,
            risk_level=risk
        )

        return JsonResponse({
            "status": "logged",
            "risk": risk
        })

    return JsonResponse({"error": "Invalid request"}, status=400)




# 🔹 Simulation Control Page
def simulation_control(request):
    sessions = SimulationSession.objects.all().order_by('-id')

    return render(request, 'scanner/simulation_control.html', {
        "sessions": sessions
    })


# 🔹 Simulation Dashboard (Results)
def simulation_dashboard(request):
    session_id = request.GET.get("session")
    risk_filter = request.GET.get("risk")

    sessions = SimulationSession.objects.all().order_by('-id')
    results = SimulationResult.objects.all()

    if session_id:
        results = results.filter(session_id=session_id)

    if risk_filter:
        results = results.filter(risk_level=risk_filter)

    results = results.order_by('-timestamp')

    return render(request, 'scanner/simulation.html', {
        "results": results,
        "sessions": sessions,
        "selected_session": session_id,
        "selected_risk": risk_filter
    })