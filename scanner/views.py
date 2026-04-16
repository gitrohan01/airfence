from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import json

from .models import NetworkObservation, AccessPoint
from .services.processor import process_network


# 🔥 API FUNCTION (IMPORTANT - DO NOT REMOVE)
@csrf_exempt
def receive_network(request):
    if request.method == "POST":
        data = json.loads(request.body)

        result = process_network(data)

        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request"}, status=400)


# 🔥 DASHBOARD VIEW
def dashboard(request):
    latest_ids = (
        NetworkObservation.objects
        .values('ssid')
        .annotate(latest_id=Max('id'))
        .values_list('latest_id', flat=True)
    )

    networks = (
        NetworkObservation.objects
        .filter(id__in=latest_ids)
        .order_by('trust_score')
    )

    secure_count = networks.filter(classification="Secure").count()
    risky_count = networks.filter(classification="Risky").count()
    critical_count = networks.filter(classification="Critical").count()

    return render(request, 'scanner/dashboard.html', {
        'networks': networks,
        'secure_count': secure_count,
        'risky_count': risky_count,
        'critical_count': critical_count
    })


from django.http import FileResponse
from .utils.report_generator import generate_pdf, generate_excel
import os


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

    # 🔍 Search
    if query:
        networks = networks.filter(ssid__icontains=query)

    # 🔍 Filter
    if filter_type:
        networks = networks.filter(classification=filter_type)

    networks = networks.order_by('trust_score')

    # Counts
    secure_count = networks.filter(classification="Secure").count()
    risky_count = networks.filter(classification="Risky").count()
    critical_count = networks.filter(classification="Critical").count()

    # 🚨 Alert
    alert = critical_count > 0

    return render(request, 'scanner/dashboard.html', {
        'networks': networks,
        'secure_count': secure_count,
        'risky_count': risky_count,
        'critical_count': critical_count,
        'alert': alert
    })


from django.shortcuts import render
from .models import AccessPoint

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

    return render(request, 'scanner/evil_twins.html', {
        "results": results
    })


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

from .models import SimulationResult, SimulationSession

@csrf_exempt
def log_simulation(request):
    if request.method == "POST":
        data = json.loads(request.body)

        session_id = data.get("session_id")
        device_id = data.get("device_id")
        action = data.get("action")

        session = SimulationSession.objects.get(id=session_id)

        # 🔥 Risk logic
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


from django.views.decorators.csrf import csrf_exempt
from .models import SimulationSession

@csrf_exempt
def start_simulation(request):
    if request.method == "POST":
        session = SimulationSession.objects.create(name="Security Test")

        return JsonResponse({
            "status": "started",
            "session_id": session.id
        })

    return JsonResponse({"error": "Use POST request"}, status=400)


from .models import SimulationResult, SimulationSession

def simulation_dashboard(request):
    session_id = request.GET.get("session")

    sessions = SimulationSession.objects.all().order_by('-id')

    results = SimulationResult.objects.all()

    if session_id:
        results = results.filter(session_id=session_id)

    results = results.order_by('-timestamp')

    return render(request, 'scanner/simulation.html', {
        "results": results,
        "sessions": sessions,
        "selected_session": session_id
    })