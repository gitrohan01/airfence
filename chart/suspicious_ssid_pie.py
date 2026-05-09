import os
import sys

# -----------------------------------------
# ADD PROJECT ROOT TO PYTHON PATH
# -----------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(BASE_DIR)

# -----------------------------------------
# DJANGO SETUP
# -----------------------------------------

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "airfence.settings"
)

import django
django.setup()

# -----------------------------------------
# IMPORTS
# -----------------------------------------

import matplotlib.pyplot as plt

from scanner.models import NetworkObservation

# -----------------------------------------
# COUNT UNIQUE NETWORKS
# -----------------------------------------

suspicious = (
    NetworkObservation.objects
    .filter(is_suspicious_name=True)
    .values("access_point__bssid")
    .distinct()
    .count()
)

normal = (
    NetworkObservation.objects
    .filter(is_suspicious_name=False)
    .values("access_point__bssid")
    .distinct()
    .count()
)

# -----------------------------------------
# PREPARE DATA
# -----------------------------------------

labels = [
    "Normal SSIDs",
    "Suspicious SSIDs"
]

sizes = [
    normal,
    suspicious
]

# -----------------------------------------
# CREATE PIE CHART
# -----------------------------------------

plt.figure(figsize=(8, 8))

plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

# -----------------------------------------
# LABELS
# -----------------------------------------

plt.title(
    "AirFence Suspicious SSID Detection"
)

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "suspicious_ssid_pie.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.close()