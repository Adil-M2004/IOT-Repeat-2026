import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    # Fetch variables securely, avoiding hardcoded plain text
    PUBNUB_SUBSCRIBE_KEY = os.getenv("PUBNUB_SUBSCRIBE_KEY")
    PUBNUB_PUBLISH_KEY = os.getenv("PUBNUB_PUBLISH_KEY")
    PUBNUB_SECRET_KEY = os.getenv("PUBNUB_SECRET_KEY")
    PUBNUB_CIPHER_KEY = os.getenv("PUBNUB_CIPHER_KEY")
    
    # Database config placeholder for later
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///iot_data.db")