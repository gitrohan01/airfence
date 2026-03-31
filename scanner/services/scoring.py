def calculate_trust_score(classification, risk_score, is_suspicious, is_evil):
    base = 5.0

    if classification == "Critical":
        base -= 3
    elif classification == "Risky":
        base -= 2

    if is_suspicious:
        base -= 1

    if is_evil:
        base -= 1

    base -= risk_score  # fine adjustment

    return max(0, round(base, 2))