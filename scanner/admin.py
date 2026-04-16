from django.contrib import admin
from .models import (
    AccessPoint,
    ScanSession,
    NetworkObservation,
    SimulationSession,
    SimulationResult
)


# 🔹 Access Point Admin
@admin.register(AccessPoint)
class AccessPointAdmin(admin.ModelAdmin):
    list_display = ('ssid', 'bssid')


# 🔹 Scan Session Admin
@admin.register(ScanSession)
class ScanSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_name', 'location', 'timestamp')


# 🔹 Network Observation Admin
@admin.register(NetworkObservation)
class NetworkObservationAdmin(admin.ModelAdmin):
    list_display = (
        'ssid',
        'encryption',
        'rssi',
        'channel',
        'classification',
        'trust_score',
        'is_evil_twin'
    )
    list_filter = ('classification', 'encryption', 'is_evil_twin')
    search_fields = ('ssid', 'access_point__bssid')


# 🔥 NEW MODELS (simple registration is fine)
admin.site.register(SimulationSession)
admin.site.register(SimulationResult)