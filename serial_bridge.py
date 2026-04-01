import serial
import json
import requests

# 🔌 Change COM port if needed
SERIAL_PORT = 'COM4'
BAUD_RATE = 115200

# Django API
API_URL = "http://127.0.0.1:8000/api/network/"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

print("🚀 Serial Bridge Started...")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()

        if not line:
            continue

        if line.startswith("START"):
            continue

        # Try parsing JSON
        data = json.loads(line)

        print("📡 Sending:", data)

        response = requests.post(API_URL, json=data)

        print("✅ Response:", response.json())

    except json.JSONDecodeError:
        # Ignore non-JSON lines
        continue

    except Exception as e:
        print("❌ Error:", e)