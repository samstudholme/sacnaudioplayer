# Raspberry Pi Audio Player

This project is a lightweight web application designed to run on a Raspberry Pi, allowing users to upload and manage audio tracks. The application provides functionality to specify ACN universe, address, and playback channel for each track, as well as control the master volume for all tracks. 

## Project Written using Copilot (may not work)

## Project Structure

```
pi-audio-player
├── src
│   ├── main.py          # Entry point of the application
│   ├── routes.py        # Defines the web application routes
│   ├── audio
│   │   └── __init__.py  # Logic for managing audio tracks
│   ├── templates
│   │   └── index.html    # HTML template for the web interface
│   ├── static
│   │   └── style.css     # CSS styles for the web application
│   └── config.py        # Configuration settings for the application
├── requirements.txt      # Lists project dependencies
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/samstudholme/sacnaudioplayer.git
   cd pi-audio-player
   ```

2. **Install dependencies:**
   Make sure you have Python and pip installed on your Raspberry Pi. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Navigate to the `src` directory and run:
   ```bash
   python main.py
   ```

4. **Access the web interface:**
   Open a web browser and go to `http://<raspberry-pi-ip>:5000` to access the audio player interface.

## Usage Guidelines

- Upload audio tracks using the provided interface.
- Specify the ACN universe, address, and playback channel for each track.
- Control the master volume for all tracks from the web interface.
- Enjoy your audio playback on the Raspberry Pi!

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.
