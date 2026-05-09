import serial
import json
import requests
import os
import time

SERIAL_PORT = 'COM4'
BAUD_RATE = 115200

API_NETWORK = "http://127.0.0.1:8000/api/network/"
API_SIM_LOG = "http://127.0.0.1:8000/api/simulation/log/"

COMMAND_FILE = "command.txt"
SESSION_FILE = "session.txt"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# 🔥 Track unique devices per session
seen_devices = set()

print("🚀 Serial Bridge Running...")


# 🔹 Get current session ID
def get_session_id():
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                val = f.read().strip()
                return int(val) if val else None
    except:
        pass
    return None


# 🔹 Handle commands from Django
def check_command():
    global seen_devices

    try:
        if os.path.exists(COMMAND_FILE):
            with open(COMMAND_FILE, "r") as f:
                cmd = f.read().strip()

            if cmd:
                ser.write((cmd + "\n").encode())
                time.sleep(0.2)  # 🔥 ensures ESP reads command

                print("➡️ Sent to ESP:", cmd)

                # 🔥 Reset device tracking on new simulation
                if cmd == "START_SIM":
                    seen_devices.clear()

                # Clear command file
                open(COMMAND_FILE, "w").close()

    except Exception as e:
        print("❌ Command Error:", e)


# 🔁 MAIN LOOP
while True:
    try:
        check_command()

        line = ser.readline().decode('utf-8', errors='ignore').strip()

        if not line:
            continue

        # Ignore debug markers
        if line.startswith("MODE") or line.startswith("SCAN"):
            print("ℹ️", line)
            continue

        data = json.loads(line)

        # 🔹 NETWORK DATA
        if "ssid" in data:
            print("📡 Network:", data)

            try:
                res = requests.post(API_NETWORK, json=data, timeout=2)
                print("✅ Network Sent:", res.status_code)
            except Exception as e:
                print("❌ Network API Error:", e)

        # 🔹 SIMULATION DATA (WITH DUPLICATE FILTER)
        elif "device_id" in data:
            session_id = get_session_id()

            if session_id:
                key = f"{session_id}_{data['device_id']}"

                # 🚫 Skip duplicate devices
                if key in seen_devices:
                    continue

                seen_devices.add(key)

                payload = {
                    "session_id": session_id,
                    "device_id": data["device_id"],
                    "action": data.get("action", "connected")
                }

                print("👤 Device:", payload)

                try:
                    res = requests.post(API_SIM_LOG, json=payload, timeout=2)
                    print("✅ Sim Log Sent:", res.status_code)
                except Exception as e:
                    print("❌ Simulation API Error:", e)

            else:
                print("⚠️ No active session, ignoring device")

    except json.JSONDecodeError:
        continue
    except Exception as e:
        print("❌ Error:", e)

    time.sleep(0.1)