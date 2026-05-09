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
# FETCH ENCRYPTION DATA
# -----------------------------------------

encryptions = NetworkObservation.objects.values_list(
    "encryption",
    flat=True
)

counts = Counter(encryptions)

labels = list(counts.keys())
sizes = list(counts.values())

# -----------------------------------------
# CREATE PIE CHART
# -----------------------------------------

plt.figure(figsize=(8, 8))

plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

plt.title("Encryption-wise Security Distribution")

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "encryption_pie_chart.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.show()