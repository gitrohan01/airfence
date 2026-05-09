import socket
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
    auto_stop_inactive_sessions()

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

        # 🔥 write command
        with open("command.txt", "w") as f:
            f.write("START_SIM")

        # 🔥 store session
        with open("session.txt", "w") as f:
            f.write(str(session.id))

        return JsonResponse({
            "status": "started",
            "session_id": session.id
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

# 🔹 Stop Simulation

from django.utils.timezone import now

@csrf_exempt
def stop_simulation(request):
    if request.method == "POST":

        # 🔥 get latest active session
        session = SimulationSession.objects.filter(status='active').last()

        if not session:
            return JsonResponse({"error": "No active session"}, status=400)

        session.status = "stopped"
        session.ended_at = now()
        session.save()

        # 🔥 send STOP command to ESP
        with open("command.txt", "w") as f:
            f.write("STOP_SIM")

        # 🔥 clear session tracking
        open("session.txt", "w").close()

        return JsonResponse({
            "status": "stopped",
            "session_id": session.id
        })

    return JsonResponse({"error": "Invalid request"}, status=400)




# 🔹 Log Simulation Activity


@csrf_exempt
def log_simulation(request):
    if request.method == "POST":
        data = json.loads(request.body)

        session_id = data.get("session_id")
        device_id = data.get("device_id")
        action = data.get("action", "connected")

        if not session_id or not device_id:
            return JsonResponse({"error": "Missing data"}, status=400)

        try:
            session = SimulationSession.objects.get(id=session_id)
        except SimulationSession.DoesNotExist:
            return JsonResponse({"error": "Invalid session"}, status=404)

        # 🔥 UPDATE LAST ACTIVITY (CRITICAL)
        session.last_activity = now()
        session.save()

        # Save result
        SimulationResult.objects.create(
            session=session,
            device_id=device_id,
            action=action,
            risk_level="High"
        )

        return JsonResponse({"status": "logged"})

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
    auto_stop_inactive_sessions()

    sessions = SimulationSession.objects.all().order_by('-id')

    latest_ids = (
        SimulationResult.objects
        .values('device_id', 'session')
        .annotate(latest_id=Max('id'))
        .values_list('latest_id', flat=True)
    )

    results = SimulationResult.objects.filter(id__in=latest_ids)

    # ✅ SAME INDENT LEVEL
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





from datetime import timedelta

def auto_stop_inactive_sessions():
    threshold = now() - timedelta(seconds=60)  # 60 sec inactivity

    sessions = SimulationSession.objects.filter(
        status='active',
        last_activity__lt=threshold
    )

    for s in sessions:
        s.status = 'stopped'
        s.ended_at = now()
        s.save()




def simulation_sessions(request):
    sessions = SimulationSession.objects.all().order_by('-started_at')

    return render(request, "scanner/sessions.html", {
        "sessions": sessions
    })


def session_detail(request, session_id):
    session = SimulationSession.objects.get(id=session_id)

    latest_ids = (
        SimulationResult.objects
        .filter(session=session)
        .values('device_id')
        .annotate(latest_id=Max('id'))
        .values_list('latest_id', flat=True)
    )

    results = SimulationResult.objects.filter(id__in=latest_ids).order_by('-timestamp')

    return render(request, "scanner/session_detail.html", {
        "session": session,
        "results": results
    })




from django.http import FileResponse
from django.db.models import Max, Count
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def download_session_pdf(request, session_id):
    session = SimulationSession.objects.get(id=session_id)

    latest_ids = (
        SimulationResult.objects
        .filter(session=session)
        .values('device_id')
        .annotate(latest_id=Max('id'))
        .values_list('latest_id', flat=True)
    )

    results = SimulationResult.objects.filter(id__in=latest_ids)

    # 📊 Summary
    total_devices = results.count()
    high_risk = results.filter(risk_level="High").count()

    file_path = f"session_{session_id}.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph(f"Session Report: {session.name}", styles['Title']))
    elements.append(Paragraph(f"Session ID: {session.id}", styles['Normal']))
    elements.append(Paragraph(f"Total Devices: {total_devices}", styles['Normal']))
    elements.append(Paragraph(f"High Risk Devices: {high_risk}", styles['Normal']))

    # Table Data
    table_data = [["Device", "Action", "Risk", "Time"]]

    for r in results:
        table_data.append([
            r.device_id,
            r.action,
            r.risk_level,
            r.timestamp.strftime("%Y-%m-%d %H:%M")
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)

    return FileResponse(open(file_path, 'rb'), as_attachment=True)