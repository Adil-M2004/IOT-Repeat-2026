import sqlite3
from config import Config
from flask import Flask, jsonify, render_template, request
from pubnub.models.consumer.v3.channel import Channel
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

app = Flask(__name__)
app.config.from_object(Config)

# Database Setup
DB_FILE = "sensor_data.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity REAL,
            motion TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()  # Initialize table on startup

# PubNub Config
pnconfig = PNConfiguration()
pnconfig.subscribe_key = app.config["PUBNUB_SUBSCRIBE_KEY"]
pnconfig.publish_key = app.config["PUBNUB_PUBLISH_KEY"]
pnconfig.secret_key = app.config["PUBNUB_SECRET_KEY"]
pnconfig.cipher_key = app.config.get("PUBNUB_CIPHER_KEY")
pnconfig.uuid = "flask-backend-server"
pubnub = PubNub(pnconfig)


@app.route("/")
def index():
    return render_template(
        "index.html",
        pubnub_sub_key=app.config["PUBNUB_SUBSCRIBE_KEY"],
        pubnub_cipher_key=app.config.get("PUBNUB_CIPHER_KEY", ""),
    )


# API to store incoming sensor payload into SQLite
@app.route("/api/telemetry", methods=["POST"])
def save_telemetry():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO telemetry (temperature, humidity, motion)
        VALUES (?, ?, ?)
    """,
        (
            data.get("temperature"),
            data.get("humidity"),
            str(data.get("motion")),
        ),
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201


# API to fetch historical sensor data for Chart.js
@app.route("/api/history", methods=["GET"])
def get_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, temperature, humidity, motion FROM telemetry ORDER BY id DESC LIMIT 20"
    )
    rows = cursor.fetchall()
    conn.close()

    history = [
        {
            "timestamp": r[0],
            "temperature": r[1],
            "humidity": r[2],
            "motion": r[3],
        }
        for r in reversed(rows)
    ]
    return jsonify(history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)