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

evil_twins = (
    NetworkObservation.objects
    .filter(is_evil_twin=True)
    .values("access_point__bssid")
    .distinct()
    .count()
)

legitimate = (
    NetworkObservation.objects
    .filter(is_evil_twin=False)
    .values("access_point__bssid")
    .distinct()
    .count()
)

# -----------------------------------------
# PREPARE DATA
# -----------------------------------------

labels = [
    "Legitimate Networks",
    "Evil Twin Networks"
]

sizes = [
    legitimate,
    evil_twins
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

plt.title(
    "AirFence Evil Twin Detection Statistics"
)

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "evil_twin_pie_chart.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.close()