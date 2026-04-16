from django.db import models


# 🔹 Access Point (Unique network device)
class AccessPoint(models.Model):
    ssid = models.CharField(max_length=100)
    bssid = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.ssid} ({self.bssid})"


# 🔹 Scan Session (Each scan event)
class ScanSession(models.Model):
    device_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} - {self.device_name}"


# 🔹 Core Observation Table (ML + Intelligence)
class NetworkObservation(models.Model):
    access_point = models.ForeignKey(AccessPoint, on_delete=models.CASCADE)
    session = models.ForeignKey(ScanSession, on_delete=models.CASCADE)

    # Basic Wi-Fi Data
    ssid = models.CharField(max_length=100)
    encryption = models.CharField(max_length=50)
    rssi = models.IntegerField()
    channel = models.IntegerField()

    # Intelligence Features
    is_suspicious_name = models.BooleanField(default=False)
    duplicate_count = models.IntegerField(default=1)
    is_evil_twin = models.BooleanField(default=False)

    # Decision Outputs (Rule-Based)
    classification = models.CharField(max_length=20)
    risk_score = models.FloatField(default=0)   # 0–1
    trust_score = models.FloatField(default=0)  # 0–5

    # 🔥 NEW: ML Output
    ml_classification = models.CharField(max_length=20, null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ssid} - {self.classification}"
    

# 🔥 Simulation Session (each awareness test)
class SimulationSession(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Simulation {self.id} - {self.name}"


# 🔥 Simulation Result (user behavior)
class SimulationResult(models.Model):
    session = models.ForeignKey(SimulationSession, on_delete=models.CASCADE)

    device_id = models.CharField(max_length=100)
    action = models.CharField(max_length=50)  # connected / completed
    risk_level = models.CharField(max_length=20)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_id} - {self.risk_level}"