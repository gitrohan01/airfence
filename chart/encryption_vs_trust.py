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

from collections import defaultdict
import matplotlib.pyplot as plt

from scanner.models import NetworkObservation

# -----------------------------------------
# FETCH UNIQUE NETWORK DATA
# -----------------------------------------

observations = (
    NetworkObservation.objects
    .values(
        "encryption",
        "trust_score",
        "access_point__bssid"
    )
    .distinct()
)

# -----------------------------------------
# GROUP TRUST SCORES
# -----------------------------------------

trust_groups = defaultdict(list)

for obs in observations:

    encryption = obs["encryption"]
    trust_score = obs["trust_score"]

    trust_groups[encryption].append(trust_score)

# -----------------------------------------
# CALCULATE AVERAGES
# -----------------------------------------

labels = []
avg_scores = []

for encryption, scores in trust_groups.items():

    avg = sum(scores) / len(scores)

    labels.append(encryption)
    avg_scores.append(round(avg, 2))

# -----------------------------------------
# CREATE BAR CHART
# -----------------------------------------

plt.figure(figsize=(10, 6))

bars = plt.bar(
    labels,
    avg_scores
)

# -----------------------------------------
# ADD VALUES ABOVE BARS
# -----------------------------------------

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.2f}",
        ha='center',
        va='bottom'
    )

# -----------------------------------------
# LABELS
# -----------------------------------------

plt.xlabel("Encryption Type")
plt.ylabel("Average Trust Score")

plt.title(
    "Encryption vs Average Trust Score"
)

plt.grid(axis='y')

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "encryption_vs_trust.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.close()