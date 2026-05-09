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
# FETCH DATA
# -----------------------------------------

observations = (
    NetworkObservation.objects
    .values_list("timestamp", flat=True)
)

# -----------------------------------------
# GROUP BY DATE
# -----------------------------------------

date_counts = Counter()

for timestamp in observations:

    if timestamp:
        date = timestamp.date()
        date_counts[date] += 1

# -----------------------------------------
# SORT DATA
# -----------------------------------------

sorted_dates = sorted(date_counts.items())

x = [str(item[0]) for item in sorted_dates]
y = [item[1] for item in sorted_dates]

# -----------------------------------------
# CREATE LINE CHART
# -----------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    x,
    y,
    marker='o'
)

# -----------------------------------------
# LABELS
# -----------------------------------------

plt.xlabel("Date")
plt.ylabel("Number of Observations")

plt.title(
    "AirFence Scan Activity Timeline"
)

plt.xticks(rotation=45)

plt.grid(True)

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "scan_activity_timeline.png"
)

plt.savefig(
    output_path,
    bbox_inches='tight'
)

print(f"Chart saved to: {output_path}")

plt.close()