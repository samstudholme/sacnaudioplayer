from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import subprocess

audio_bp = Blueprint('audio', __name__)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@audio_bp.route('/')
def index():
    return render_template('index.html')

@audio_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    return jsonify({'error': 'File type not allowed'}), 400

@audio_bp.route('/play', methods=['POST'])
def play_audio():
    data = request.json
    universe = data.get('universe')
    address = data.get('address')
    channel = data.get('channel')
    filename = data.get('filename')
    # Logic to play audio based on universe, address, channel, and filename
    return jsonify({'message': 'Playing audio', 'filename': filename}), 200

@audio_bp.route('/volume', methods=['POST'])
def set_volume():
    volume = request.json.get('volume')
    # Logic to set master volume
    return jsonify({'message': 'Volume set', 'volume': volume}), 200

@app.route('/set_ip', methods=['POST'])
def set_ip():
    ip = request.form.get('ip')
    router = request.form.get('router')
    dns = request.form.get('dns')
    dhcpcd_conf = '/etc/dhcpcd.conf'

    if ip and router and dns:
        static_conf = (
            f"\ninterface eth0\n"
            f"static ip_address={ip}/24\n"
            f"static routers={router}\n"
            f"static domain_name_servers={dns}\n"
        )
        try:
            # Backup current config
            subprocess.run(['sudo', 'cp', dhcpcd_conf, dhcpcd_conf + '.bak'], check=True)
            # Remove previous static config for eth0
            with open(dhcpcd_conf, 'r') as f:
                lines = f.readlines()
            with open(dhcpcd_conf, 'w') as f:
                skip = False
                for line in lines:
                    if line.strip().startswith('interface eth0'):
                        skip = True
                    if not skip:
                        f.write(line)
                    if skip and line.strip() == '':
                        skip = False
                f.write(static_conf)
            # Restart networking
            subprocess.run(['sudo', 'systemctl', 'restart', 'dhcpcd'], check=True)
            flash('Static IP set. Please reboot for changes to take effect.', 'success')
        except Exception as e:
            flash(f'Failed to set static IP: {e}', 'error')
    else:
        # If not set, fallback to DHCP
        try:
            subprocess.run(['sudo', 'cp', dhcpcd_conf + '.bak', dhcpcd_conf], check=True)
            subprocess.run(['sudo', 'systemctl', 'restart', 'dhcpcd'], check=True)
            flash('Reverted to DHCP.', 'success')
        except Exception as e:
            flash(f'Failed to revert to DHCP: {e}', 'error')
    return redirect(url_for('index'))