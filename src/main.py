import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash
from werkzeug.utils import secure_filename
from audio import AudioManager
import subprocess

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # Needed for flash messages

audio_manager = AudioManager()

# Start auto-play tracks on boot
def start_autoplay_tracks():
    for filename in audio_manager.get_autoplay():
        if filename in audio_manager.get_tracks():
            audio_manager.play_track(filename)
# Call after all tracks are loaded
@app.before_first_request
def boot_autoplay():
    start_autoplay_tracks()

@app.route('/')
def index():
    return render_template('index.html', tracks=audio_manager.get_tracks(), master_volume=audio_manager.master_volume, autoplay_tracks=audio_manager.get_autoplay())

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and audio_manager.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        audio_manager.add_track(filename, {
            'universe': request.form.get('universe', ''),
            'address': request.form.get('address', ''),
            'channel': request.form.get('channel', ''),
            'playing': False,
            'volume': 1.0,
            'thread': None,
            'stop_event': None
        })
        flash('File uploaded successfully', 'success')
        return redirect(url_for('index'))
    flash('Invalid file type', 'error')
    return redirect(url_for('index'))

@app.route('/play/<filename>', methods=['POST'])
def play_track(filename):
    channel = int(request.form.get('channel', 0))
    track = audio_manager.get_tracks().get(filename)
    if not track:
        return jsonify(success=False)
    if channel == 255:
        audio_manager.play_track(filename)
    elif channel == 0:
        audio_manager.stop_track(filename)
    track['channel'] = channel
    return jsonify(success=True)

@app.route('/set_master_volume', methods=['POST'])
def set_master_volume():
    audio_manager.set_master_volume(request.form.get('volume', 1.0))
    return jsonify(success=True)

@app.route('/set_autoplay/<filename>', methods=['POST'])
def set_autoplay(filename):
    enabled = request.form.get('autoplay') == 'on'
    audio_manager.set_autoplay(filename, enabled)
    flash(f'Autoplay {"enabled" if enabled else "disabled"} for {filename}', 'success')
    return redirect(url_for('index'))

@app.route('/reboot', methods=['POST'])
def reboot():
    flash('Rebooting system...', 'info')
    subprocess.Popen(['sudo', 'reboot'])
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)