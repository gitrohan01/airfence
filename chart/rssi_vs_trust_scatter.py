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
# FETCH UNIQUE DATA
# -----------------------------------------

observations = (
    NetworkObservation.objects
    .values(
        "rssi",
        "trust_score",
        "classification",
        "access_point__bssid"
    )
    .distinct()
)

# -----------------------------------------
# PREPARE DATA
# -----------------------------------------

x_secure = []
y_secure = []

x_risky = []
y_risky = []

x_critical = []
y_critical = []

x_unknown = []
y_unknown = []

# -----------------------------------------
# CLASSIFY POINTS
# -----------------------------------------

for obs in observations:

    rssi = obs["rssi"]
    trust = obs["trust_score"]
    classification = obs["classification"]

    if classification == "Secure":
        x_secure.append(rssi)
        y_secure.append(trust)

    elif classification == "Risky":
        x_risky.append(rssi)
        y_risky.append(trust)

    elif classification == "Critical":
        x_critical.append(rssi)
        y_critical.append(trust)

    else:
        x_unknown.append(rssi)
        y_unknown.append(trust)

# -----------------------------------------
# CREATE SCATTER PLOT
# -----------------------------------------

plt.figure(figsize=(10, 6))

plt.scatter(
    x_secure,
    y_secure,
    label="Secure"
)

plt.scatter(
    x_risky,
    y_risky,
    label="Risky"
)

plt.scatter(
    x_critical,
    y_critical,
    label="Critical"
)

plt.scatter(
    x_unknown,
    y_unknown,
    label="Unknown"
)

# -----------------------------------------
# LABELS
# -----------------------------------------

plt.xlabel("RSSI Signal Strength")
plt.ylabel("Trust Score")

plt.title(
    "RSSI vs Trust Score Analysis"
)

plt.legend()

plt.grid(True)

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "rssi_vs_trust_scatter.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.close()