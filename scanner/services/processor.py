from scanner.models import AccessPoint, ScanSession, NetworkObservation
from .classifier import classify_encryption
from .detector import is_suspicious_ssid, detect_duplicates
from .scoring import calculate_trust_score
from scanner.ml.predict import predict_network


def process_network(data):
    ssid = data["ssid"]
    bssid = data["bssid"]
    encryption = data["encryption"]
    rssi = data["rssi"]
    channel = data["channel"]

    # 1. Get/Create Access Point
    ap, _ = AccessPoint.objects.get_or_create(
        bssid=bssid,
        defaults={"ssid": ssid}
    )

    # 2. Create Session
    session = ScanSession.objects.create(device_name="ESP32")

    # 3. Rule-Based Classification
    classification, risk_score = classify_encryption(encryption)

    # 4. Detection
    suspicious = is_suspicious_ssid(ssid)
    duplicate_count, is_evil = detect_duplicates(ssid)

    # 5. Trust Score
    trust_score = calculate_trust_score(
        classification,
        risk_score,
        suspicious,
        is_evil
    )

    # 🔥 6. ML Prediction (NEW)
    ml_prediction = predict_network({
        "encryption": encryption,
        "rssi": rssi,
        "channel": channel
    })

    # 7. Save Observation (UPDATED)
    NetworkObservation.objects.create(
        access_point=ap,
        session=session,
        ssid=ssid,
        encryption=encryption,
        rssi=rssi,
        channel=channel,
        is_suspicious_name=suspicious,
        duplicate_count=duplicate_count,
        is_evil_twin=is_evil,
        classification=classification,
        risk_score=risk_score,
        trust_score=trust_score,
        ml_classification=ml_prediction   # 🔥 ADDED
    )

    # 8. Return Response
    return {
        "status": "success",
        "classification": classification,
        "ml_prediction": ml_prediction,   # 🔥 ADDED
        "trust_score": trust_score
    }