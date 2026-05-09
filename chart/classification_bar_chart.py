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

from collections import Counter
import matplotlib.pyplot as plt

from scanner.models import NetworkObservation

# -----------------------------------------
# FETCH UNIQUE NETWORK CLASSIFICATIONS
# -----------------------------------------

unique_networks = (
    NetworkObservation.objects
    .values(
        "access_point__bssid",
        "classification"
    )
    .distinct()
)

counts = Counter()

for item in unique_networks:
    classification = item["classification"]
    counts[classification] += 1

# -----------------------------------------
# PREPARE DATA
# -----------------------------------------

labels = [
    "Secure",
    "Risky",
    "Critical",
    "Unknown"
]

values = [
    counts.get("Secure", 0),
    counts.get("Risky", 0),
    counts.get("Critical", 0),
    counts.get("Unknown", 0)
]

# -----------------------------------------
# CREATE BAR CHART
# -----------------------------------------

plt.figure(figsize=(8, 6))

bars = plt.bar(
    labels,
    values
)

# -----------------------------------------
# ADD VALUES ABOVE BARS
# -----------------------------------------

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        str(height),
        ha='center',
        va='bottom'
    )

# -----------------------------------------
# LABELS
# -----------------------------------------

plt.xlabel("Network Classification")
plt.ylabel("Unique Network Count")

plt.title(
    "AirFence Threat Classification Distribution"
)

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "classification_bar_chart.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.close()