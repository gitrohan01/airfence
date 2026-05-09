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
# FETCH UNIQUE CHANNEL DATA
# -----------------------------------------

networks = (
    NetworkObservation.objects
    .values(
        "channel",
        "access_point__bssid"
    )
    .distinct()
)

# -----------------------------------------
# COUNT CHANNELS
# -----------------------------------------

counts = Counter()

for item in networks:
    channel = item["channel"]
    counts[channel] += 1

# -----------------------------------------
# SORT CHANNELS
# -----------------------------------------

sorted_channels = sorted(counts.items())

labels = [str(ch[0]) for ch in sorted_channels]
values = [ch[1] for ch in sorted_channels]

# -----------------------------------------
# CREATE BAR CHART
# -----------------------------------------

plt.figure(figsize=(10, 6))

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

plt.xlabel("Wi-Fi Channel")
plt.ylabel("Unique Network Count")

plt.title(
    "AirFence Wi-Fi Channel Usage Analysis"
)

plt.grid(axis='y')

# -----------------------------------------
# SAVE CHART
# -----------------------------------------

output_path = os.path.join(
    BASE_DIR,
    "chart",
    "channel_usage_bar_chart.png"
)

plt.savefig(output_path)

print(f"Chart saved to: {output_path}")

plt.close()