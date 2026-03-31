SUSPICIOUS_KEYWORDS = [
    "free", "wifi", "public", "guest", "5g", "unlimited"
]

def is_suspicious_ssid(ssid):
    ssid_lower = ssid.lower()

    for word in SUSPICIOUS_KEYWORDS:
        if word in ssid_lower:
            return True
    return False


from scanner.models import AccessPoint

def detect_duplicates(ssid):
    count = AccessPoint.objects.filter(ssid=ssid).count()
    is_evil = count > 1
    return count, is_evil