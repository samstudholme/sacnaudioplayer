import os
import threading
from pydub import AudioSegment
import simpleaudio as sa
from src import config

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

class AudioManager:
    def __init__(self):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        self.tracks = {}  # filename: {info}
        self.master_volume = 1.0
        self.autoplay_tracks = set(config.load_autoplay())

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def add_track(self, filename, info):
        self.tracks[filename] = info

    def get_tracks(self):
        return self.tracks

    def play_track(self, filename):
        track = self.tracks.get(filename)
        if not track or track.get('playing'):
            return
        track['playing'] = True
        track['stop_event'] = threading.Event()

        def loop_play():
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            audio = AudioSegment.from_file(filepath)
            audio = audio - (1.0 - self.master_volume) * 60  # crude volume control
            while not track['stop_event'].is_set():
                play_obj = sa.play_buffer(audio.raw_data, num_channels=audio.channels,
                                          bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
                play_obj.wait_done()

        t = threading.Thread(target=loop_play, daemon=True)
        track['thread'] = t
        t.start()

    def stop_track(self, filename):
        track = self.tracks.get(filename)
        if not track or not track.get('playing'):
            return
        track['stop_event'].set()
        track['playing'] = False

    def set_master_volume(self, volume):
        try:
            self.master_volume = float(volume)
        except ValueError:
            pass

    def set_autoplay(self, filename, enabled):
        if enabled:
            self.autoplay_tracks.add(filename)
        else:
            self.autoplay_tracks.discard(filename)
        config.save_autoplay(list(self.autoplay_tracks))

    def get_autoplay(self):
        return self.autoplay_tracks