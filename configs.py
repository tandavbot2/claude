import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", ""))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    FSUB = os.getenv("FSUB", "")
    CHID = int(os.getenv("CHID", "-1002177395485"))
    SUDO = list(map(int, os.getenv("SUDO", "").split()))
    MONGO_URI = os.getenv("MONGO_URI", "")
    
    # Required channels configuration
    REQUIRED_CHANNELS = os.getenv("REQUIRED_CHANNELS", "Or3kii").split(',')
    
    # New configurations
    BOT_NAME = os.getenv("BOT_NAME", "TandavBot")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "")
    BOT_VERSION = os.getenv("BOT_VERSION", "1.0.0")
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Webhook configuration (for production deployment)
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    WEBHOOK_PORT = int(os.getenv("PORT", 8443))  # Default port for Heroku
    
    # Rate limiting
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 5))  # Number of requests per minute
    
    # Feature flags
    ENABLE_BROADCAST = os.getenv("ENABLE_BROADCAST", "True").lower() == "true"
    ENABLE_CHANNEL_CHECK = os.getenv("ENABLE_CHANNEL_CHECK", "True").lower() == "true"

    @classmethod
    def validate(cls):
        required_fields = ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URI"]
        for field in required_fields:
            if not getattr(cls, field):
                raise ValueError(f"{field} must be set in environment variables")

cfg = Config()

# Validate configuration
cfg.validate()
