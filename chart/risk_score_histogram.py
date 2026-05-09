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
# FETCH UNIQUE RISK SCORES
# -----------------------------------------

observations = (
    NetworkObservation.objects
    .values(
        "risk_score",
        "access_point__bssid"
    )
    .distinct()
)

risk_scores = [
    obs["risk_score"]
    for obs in observations
]

# -----------------------------------------
# CREATE HISTOGRAM
# -----------------------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    risk_scores,
    bins=10
)

# -----------------------------------------
# LABELS
# -----------------------------------------

plt.xlabel("Risk Score")
plt.ylabel("Number of Networks")

plt.title(
    "AirFence Risk Score Distribution"
)

plt.grid(axis='y')

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "risk_score_histogram.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.close()