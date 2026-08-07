import time
import random
import requests
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

# 1. Configuration
BACKEND_URL = "http://127.0.0.1:5000/api/get-device-token"
SUBSCRIBE_KEY = "sub-c-b486fa6d-5123-4efc-bacc-c70717da02b0" # Replace with your actual PubNub subscribe key
PUBLISH_KEY = "pub-c-376e76bf-9546-4ec8-82c1-c048cec37354"     # Replace with your actual PubNub publish key
CIPHER_KEY = "MySuperSecretIoTKey2026!" # Must match the cipher_key set in backend .env

# 2. Fetch secure PAM access token from backend server
print("[IoT Device] Requesting access token from backend server...")
response = requests.get(BACKEND_URL)

if response.status_code == 200:
    auth_token = response.json().get("token")
    print(f"[IoT Device] Access token retrieved successfully!")
else:
    print("[IoT Device] Failed to retrieve auth token. Exiting.")
    exit()

# 3. Initialize PubNub with token and payload encryption
pnconfig = PNConfiguration()
pnconfig.subscribe_key = SUBSCRIBE_KEY
pnconfig.publish_key = PUBLISH_KEY
pnconfig.auth_key = auth_token
pnconfig.cipher_key = CIPHER_KEY
pnconfig.uuid = "esp32-sensor-01"

pubnub = PubNub(pnconfig)

# 4. Main publish loop
def publish_sensor_data():
    while True:
        # Simulate sensor readings (e.g., DHT11 temperature & LDR light sensor)
        data = {
            "device_id": "esp32-sensor-01",
            "temperature": round(random.uniform(18.0, 28.0), 2),
            "light_level": random.randint(300, 800),
            "timestamp": int(time.time())
        }
        
        # Publish encrypted payload to 'sensor-data' channel
        pubnub.publish().channel("sensor-data").message(data).sync()
        print(f"[IoT Device] Published encrypted sensor payload: {data}")
        
        time.sleep(5)

if __name__ == "__main__":
    publish_sensor_data()