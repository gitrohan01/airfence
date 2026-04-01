# 🛡️ AirFence

AirFence is an IoT-based Wireless Access Point Security Classification System using Machine Learning.

## 🚀 Features

* Wi-Fi security classification (Secure / Risky / Critical)
* Suspicious SSID detection
* Evil twin detection (duplicate SSIDs)
* Trust score (0–5)
* Risk score (0–1)
* Django backend with API
* Real-time IoT integration (ESP32)

## 🧠 Tech Stack

* Django
* SQLite
* Python
* ESP32 (IoT)

## 📡 API Endpoint

POST /api/network/

## 🎯 Goal

To provide an intelligent decision support system for identifying secure and malicious Wi-Fi networks.


🔌 Serial Architecture (Offline Mode)

AirFence uses a serial communication bridge:

ESP32 → USB → Python (serial_bridge.py) → Django API

This allows:

Offline operation
No Wi-Fi dependency
Reliable real-time data transfer