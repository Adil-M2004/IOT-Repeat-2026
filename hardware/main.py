import time
import board
import adafruit_dht
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import requests

# Initialize DHT Sensor (connected to GPIO 4 / Pin 7)
dht_device = adafruit_dht.DHT11(board.D4)  # Change to DHT22 if using DHT22

# Retrieve auth token from Flask backend
res = requests.get("http://127.0.0.1:5000/api/get-device-token")
token = res.json().get("token")

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "YOUR_SUBSCRIBE_KEY"
pnconfig.publish_key = "YOUR_PUBLISH_KEY"
pnconfig.cipher_key = "MySuperSecretIoTKey2026!"
pnconfig.auth_token = token
pnconfig.uuid = "esp32-sensor-01"

pubnub = PubNub(pnconfig)

while True:
    try:
        temp_c = dht_device.temperature
        humidity = dht_device.humidity  # DHT sensors also measure humidity!

        if temp_c is not None:
            payload = {
                'device_id': 'esp32-sensor-01',
                'temperature': round(temp_c, 2),
                'light_level': round(humidity, 2) if humidity else 0, # Map humidity to light_level or update key
                'timestamp': int(time.time())
            }

            pubnub.publish().channel("sensor-data").message(payload).sync()
            print(f"[Raspberry Pi] Real telemetry payload sent: {payload}")

    except RuntimeError:
        pass # DHT sensors occasionally drop a frame; safe to ignore
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(5)