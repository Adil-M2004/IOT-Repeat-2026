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

## 🔌 Hardware Pin Mapping

[ Hardware Sensors ]
  ├─ DHT22 Temp/Humidity (GPIO 4) ──> Linux Kernel Overlay (/sys/bus/iio/...)
  ├─ PIR Motion Sensor   (GPIO 17) ──> gpiozero Interface
  └─ Breadboard LED      (GPIO 27) ──> Hardware Visual Alert
          │
          ▼
 [ Raspberry Pi 5 (Edge Device) ] ──(temp.py)
          │
          ├──> 1. Publish Live Telemetry (JSON) ──> [ PubNub Cloud Stream ] ──┐
          │                                                                   │
          └──> 2. HTTP POST Payload ────────────> [ AWS EC2 Server ]         │
                                                         │                    │
                                                         ▼                    ▼
                                                  [ SQLite DB ] ──> [ Web Dashboard ]
                                               (sensor_data.db)   (Chart.js + Log Table)
---



## 🛠️ Software Tech Stack

* **Edge Device (Raspberry Pi 5):** Python 3, `gpiozero`, `lgpio`, `requests`, PubNub Python SDK, Linux IIO Kernel Overlays.
* **Backend Framework:** Python Flask, Gunicorn, Nginx.
* **Database:** SQLite3 (`sensor_data.db`).
* **Cloud Hosting:** AWS EC2 (Ubuntu Linux).
* **Frontend UI:** HTML5, CSS3 (CSS Grid/Flexbox), JavaScript (ES6), Chart.js, PubNub JS SDK v7.

---

## 🗄️ Database Schema

Data is automatically persisted to an SQLite database named `sensor_data.db`, located inside the backend repository directory.

### Table Name: `readings`

```sql
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    motion INTEGER NOT NULL,  -- 0 = No Motion, 1 = Motion Detected
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📡 API Endpoints

| Method | Endpoint           | Description                                                                                | Request Payload / Response                                  |
| ------ | ------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| `GET`  | `/`                | Renders the primary Flask web dashboard (`index.html`).                                    | HTML Page                                                   |
| `POST` | `/api/sensor-data` | Receives telemetry payloads from Raspberry Pi 5 and appends them to the SQLite database.   | `{ "temperature": 22.5, "humidity": 61.8, "motion": true }` |
| `GET`  | `/api/history`     | Fetches the last 20 logged readings chronologically for UI chart and table initialization. | `{ "status": "success", "data": [...] }`                    |

---

# 🚀 Installation & Setup Guide

## 1. Raspberry Pi 5 Edge Configuration

### A. Enable Hardware Kernel Overlay for DHT22

Open `/boot/firmware/config.txt` on your Raspberry Pi:

```bash
sudo nano /boot/firmware/config.txt
```

Append the following line to the bottom of the file:

```ini
dtoverlay=dht11,gpiopin=4,dht22=1
```

Save the file using **Ctrl + O**, press **Enter**, and then reboot your Raspberry Pi:

```bash
sudo reboot
```

---

### B. Clone & Configure Edge Script

Clone the repository:

```bash
git clone https://github.com/Adil-M2004/IOT-Repeat-2026.git
```

Navigate into the project directory:

```bash
cd IOT-Repeat-2026
```

Install the required Python packages:

```bash
pip install python-dotenv gpiozero pubnub requests --break-system-packages
```

Create a `.env` configuration file in the project folder:

```env
PUBNUB_SUBSCRIBE_KEY=sub-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

PUBNUB_PUBLISH_KEY=pub-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

> **Important:** Never commit your real PubNub keys or other credentials to GitHub. Add `.env` to your `.gitignore` file.

Run the edge telemetry publisher:

```bash
python3 temp.py
```

---

# 2. AWS EC2 Production Server Setup

## A. Clone Repository & Install Dependencies

Log into your AWS EC2 Ubuntu instance via SSH and configure the environment.

Clone the repository:

```bash
git clone https://github.com/Adil-M2004/IOT-Repeat-2026.git
```

Navigate to the backend directory:

```bash
cd IOT-Repeat-2026/backend
```

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install flask gunicorn pubnub python-dotenv
```

Create a `.env` file containing your production credentials:

```env
PUBNUB_SUBSCRIBE_KEY=sub-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

PUBNUB_PUBLISH_KEY=pub-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

PUBNUB_SECRET_KEY=sec-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

> **Security:** Do not upload your `.env` file or production credentials to GitHub.

---

## B. Systemd & Gunicorn Deployment

Create a systemd unit file to keep the Flask application running continuously:

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

Insert the following service definition:

```ini
[Unit]
Description=Gunicorn instance for Flask IoT App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/IOT-Repeat-2026/backend
ExecStart=/home/ubuntu/IOT-Repeat-2026/backend/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Save the file, then reload the systemd daemon:

```bash
sudo systemctl daemon-reload
```

Start the Flask application:

```bash
sudo systemctl start flaskapp
```

Enable the service so that it automatically starts when the server boots:

```bash
sudo systemctl enable flaskapp
```

You can check the status of the application using:

```bash
sudo systemctl status flaskapp
```

---

# 📸 Dashboard Interface

The web interface updates dynamically across three distinct layout components:

### 📊 Metric Cards

High-visibility numerical readouts displaying:

* **Temperature (°C)**
* **Humidity (%)**

These values provide a real-time overview of the environmental conditions detected by the Raspberry Pi 5 sensors.

### 🚨 Motion Badge

Displays the current motion detection state:

* 🔴 **YES** — flashes red when motion is detected.
* ⚫ **NO** — displays dark grey when no motion is detected.

### 📈 Telemetry Graph & Side Table

The dashboard uses **Chart.js** to plot rolling temperature and humidity trends.

The accompanying log table displays timestamped sensor readings retrieved from the SQLite database.

---
