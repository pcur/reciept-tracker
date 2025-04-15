import os
from dotenv import load_dotenv
import config.settings as settings

# Load secrets from .env into os.environ
load_dotenv()

# Helper to merge .env + settings.py into os.environ
def load_config():
    # Load safe config from settings.py
    for key in dir(settings):
        if key.isupper():
            os.environ.setdefault(key, str(getattr(settings, key)))
    
    # At this point, os.environ has both secure and safe config

load_config()
