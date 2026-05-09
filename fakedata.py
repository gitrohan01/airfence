import random
from datetime import timedelta

from django.utils.timezone import now

from scanner.models import (
    AccessPoint,
    ScanSession,
    NetworkObservation
)

# ------------------------------------
# SAMPLE DATA
# ------------------------------------

names = [
    "Airtel", "JioFiber", "BSNL", "RailWire", "ACT",
    "Aboli", "Mankudale", "Shinde", "Bhoite",
    "Nagesh", "Prakash", "Sanskruti", "Rohan",
    "Sai", "Omkar", "Tejas", "Pooja",
    "Vaishnavi", "Snehal", "Rutuja",
    "Kunal", "Saurabh", "Patil",
    "Pawar", "Deshmukh", "Salunkhe",
    "Jadhav", "OnePlus", "Galaxy",
    "vivo", "Redmi", "OPPO", "Realme"
]

suffixes = [
    "_WiFi", "_5G", "_2.4G",
    "_Home", "_Office",
    "_Guest", "_Cafe",
    "_Fiber", "_Secure"
]

encryptions = [
    "OPEN",
    "WEP",
    "WPA",
    "WPA2",
    "WPA3",
    "WPA/WPA2",
    "UNKNOWN"
]

# ------------------------------------
# CREATE SINGLE SESSION
# ------------------------------------

session = ScanSession.objects.create(
    device_name="ESP32-AirFence",
    location="Satara"
)

created = 0

# ------------------------------------
# GENERATE DATASETS
# ------------------------------------

for i in range(170):

    name = random.choice(names)

    if random.random() > 0.5:
        ssid = f"{name}{random.choice(suffixes)}"
    else:
        ssid = f"{name}_{random.randint(1000,9999)}"

    encryption = random.choice(encryptions)

    rssi = random.randint(-95, -30)

    channel = random.choice([
        1, 6, 11,
        36, 40, 44, 48,
        149, 153, 157
    ])

    # ------------------------------------
    # CREATE BSSID
    # ------------------------------------

    bssid = ":".join(
        f"{random.randint(0,255):02X}"
        for _ in range(6)
    )

    # ------------------------------------
    # CREATE ACCESS POINT
    # ------------------------------------

    access_point = AccessPoint.objects.create(
        ssid=ssid,
        bssid=bssid
    )

    # ------------------------------------
    # LOGIC
    # ------------------------------------

    if encryption == "OPEN":
        classification = "Critical"
        risk_score = round(random.uniform(0.8, 1.0), 2)
        trust_score = round(random.uniform(0.0, 1.5), 1)

    elif encryption == "WEP":
        classification = "Risky"
        risk_score = round(random.uniform(0.6, 0.8), 2)
        trust_score = round(random.uniform(1.0, 2.5), 1)

    elif encryption == "WPA":
        classification = "Risky"
        risk_score = round(random.uniform(0.4, 0.6), 2)
        trust_score = round(random.uniform(2.0, 3.5), 1)

    elif encryption == "UNKNOWN":
        classification = "Unknown"
        risk_score = round(random.uniform(0.3, 0.5), 2)
        trust_score = round(random.uniform(2.5, 4.0), 1)

    else:
        classification = "Secure"
        risk_score = round(random.uniform(0.0, 0.3), 2)
        trust_score = round(random.uniform(3.5, 5.0), 1)

    # ------------------------------------
    # FLAGS
    # ------------------------------------

    suspicious = random.choice([True, False])

    duplicate_count = random.randint(1, 5)

    evil_twin = (
        duplicate_count > 2 and
        encryption == "OPEN"
    )

    # ------------------------------------
    # CREATE OBSERVATION
    # ------------------------------------

    observation = NetworkObservation.objects.create(
        access_point=access_point,
        session=session,

        ssid=ssid,
        encryption=encryption,
        rssi=rssi,
        channel=channel,

        is_suspicious_name=suspicious,
        duplicate_count=duplicate_count,
        is_evil_twin=evil_twin,

        classification=classification,
        risk_score=risk_score,
        trust_score=trust_score,

        ml_classification=classification
    )

    # OPTIONAL RANDOMIZE TIMESTAMP
    observation.timestamp = now() - timedelta(
        days=random.randint(0, 120)
    )

    observation.save()

    created += 1

print(f"SUCCESS: Inserted {created} datasets")