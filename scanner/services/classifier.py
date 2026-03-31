def classify_encryption(encryption):
    encryption = encryption.upper()

    if "WPA3" in encryption:
        return "Secure", 0.1
    elif "WPA2" in encryption:
        return "Secure", 0.3
    elif "WPA" in encryption:
        return "Risky", 0.6
    elif "WEP" in encryption:
        return "Critical", 0.9
    elif "OPEN" in encryption:
        return "Critical", 1.0
    else:
        return "Unknown", 0.5