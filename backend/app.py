from flask import Flask, jsonify, render_template
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.v3.channel import Channel
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize PubNub with credentials & AES encryption key
pnconfig = PNConfiguration()
pnconfig.subscribe_key = app.config['PUBNUB_SUBSCRIBE_KEY']
pnconfig.publish_key = app.config['PUBNUB_PUBLISH_KEY']
pnconfig.secret_key = app.config['PUBNUB_SECRET_KEY']
pnconfig.cipher_key = app.config['PUBNUB_CIPHER_KEY']  # Payload AES Encryption
pnconfig.uuid = "flask-backend-server"

pubnub = PubNub(pnconfig)

@app.route('/')
def index():
    return render_template('index.html')

# Security Endpoint: Issue Access Tokens (PAM) to hardware devices
@app.route('/api/get-device-token', methods=['GET'])
def get_device_token():
    try:
        envelope = pubnub.grant_token() \
            .ttl(60) \
            .authorized_uuid("esp32-sensor-01") \
            .channels([
                Channel.id("sensor-data").read().write()
            ]) \
            .sync()
        
        token = envelope.result.token
        return jsonify({"status": "success", "token": token}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)