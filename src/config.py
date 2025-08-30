# Configuration settings for the audio player application

import json
import os

AUDIO_FILE_PATH = '/path/to/audio/files'
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
MAX_UPLOAD_SIZE = 16 * 1024 * 1024  # 16 MB
ACN_UNIVERSE = 1
DEFAULT_VOLUME = 0.5  # Volume range from 0.0 to 1.0

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'autoplay.json')

def load_autoplay():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return []

def save_autoplay(track_list):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(track_list, f)