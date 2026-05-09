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
import numpy as np

from scanner.models import NetworkObservation

# -----------------------------------------
# FETCH UNIQUE DATA
# -----------------------------------------

observations = (
    NetworkObservation.objects
    .values(
        "classification",
        "ml_classification",
        "access_point__bssid"
    )
    .distinct()
)

# -----------------------------------------
# COUNT CLASSIFICATIONS
# -----------------------------------------

actual_counts = Counter()
ml_counts = Counter()

for obs in observations:

    actual = obs["classification"]
    ml = obs["ml_classification"]

    actual_counts[actual] += 1

    if ml:
        ml_counts[ml] += 1

# -----------------------------------------
# LABELS
# -----------------------------------------

labels = [
    "Secure",
    "Risky",
    "Critical",
    "Unknown"
]

actual_values = [
    actual_counts.get(label, 0)
    for label in labels
]

ml_values = [
    ml_counts.get(label, 0)
    for label in labels
]

# -----------------------------------------
# BAR POSITIONS
# -----------------------------------------

x = np.arange(len(labels))
width = 0.35

# -----------------------------------------
# CREATE CHART
# -----------------------------------------

plt.figure(figsize=(10, 6))

bars1 = plt.bar(
    x - width/2,
    actual_values,
    width,
    label='Rule-Based'
)

bars2 = plt.bar(
    x + width/2,
    ml_values,
    width,
    label='ML-Based'
)

# -----------------------------------------
# ADD VALUES
# -----------------------------------------

for bar in bars1:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        str(height),
        ha='center',
        va='bottom'
    )

for bar in bars2:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        str(height),
        ha='center',
        va='bottom'
    )

# -----------------------------------------
# LABELS
# -----------------------------------------

plt.xlabel("Classification")
plt.ylabel("Unique Network Count")

plt.title(
    "Rule-Based vs ML Classification Comparison"
)

plt.xticks(x, labels)

plt.legend()

plt.grid(axis='y')

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "ml_classification_comparison.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.close()