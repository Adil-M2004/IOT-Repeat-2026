# 🏠 Smart Home Telemetry & Motion Monitoring System

An end-to-end IoT environmental monitoring system built on a **Raspberry Pi 5** and hosted on **AWS EC2**. The system reads live physical hardware metrics (temperature, humidity, motion), logs historical records to an **SQLite database**, streams low-latency telemetry using **PubNub**, and displays a real-time dark-mode web dashboard powered by **Flask** and **Chart.js**.

---

## 🌟 Key Features

* **Real-Time Environment Sensing:** Reads continuous ambient temperature and humidity data using a DHT22 sensor via native Linux IIO Kernel overlays.
* **Hardware Motion Alerts:** PIR sensor triggers local breadboard LED alerts and updates a dynamic visual badge on the web UI upon motion detection.
* **Persistent SQLite Database:** Logs all telemetry samples to a backend database, retaining queryable historical data across page reloads and server restarts.
* **PubNub Cloud Telemetry:** Low-latency WebSocket data streaming pushes sensor updates to web clients without requiring page refreshes.
* **Dual Visualization UI:** Features live numerical metric cards, an interactive Chart.js trend line graph, and a side-by-side historical log table.
* **Cloud Infrastructure:** Backend Flask API hosted on AWS EC2 behind a Gunicorn production web server.

---

## 🏗️ System Architecture & Data Flow