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