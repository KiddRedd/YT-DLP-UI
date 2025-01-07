from flask import Flask, render_template, request, jsonify, make_response
import subprocess
import os

app = Flask(__name__)

DOWNLOAD_DIR = 'downloads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    type_preference = request.form.get('type_preference', 'video')
    resolution = request.form.get('resolution', '720')  # Default to 720p if not specified

    if type_preference == 'video':
        # Check the video preference and set the appropriate resolution
        resolutions = {'360': 'bestvideo[height=360]+bestaudio/best[height=360]',
                      '720': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                      '1080': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                      '1440': 'bestvideo[height=1440]+bestaudio/best[height=1440]'}
        if resolution not in resolutions:
            return make_response(jsonify({'error': 'Invalid resolution. Please choose between 360, 720, 1080, and 1440.'}), 400)
        
        command_args = ['yt-dlp', '-f', resolutions[resolution], url]
    elif type_preference == 'audio':
        command_args = ['yt-dlp', '--extract-audio', '--audio-format', 'mp3', url]
    else:
        return make_response(jsonify({'error': 'Invalid type preference. Please choose "video" or "audio".'}), 400)

    if request.headers.get('Content-Type') == 'application/json':
        try:
            result = subprocess.run(command_args, capture_output=True, text=True)
            if result.returncode != 0:
                return make_response(jsonify({'error': result.stderr}), 500)
            else:
                return make_response(jsonify({'output': 'Your media is downloading'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    else:
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
        output_path = os.path.join(DOWNLOAD_DIR, f"{os.path.basename(url).split('?')[0]}")
        try:
            result = subprocess.run(command_args, capture_output=True, text=True)
            if result.returncode != 0:
                return render_template('download.html', error=result.stderr)
            else:
                return render_template('download.html', message='Your media has been downloaded.')
        except Exception as e:
            return render_template('download.html', error=str(e))

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_PORT', 3030))  # DEFAULTING TO PORT 3030
    app.run(host='0.0.0.0', port=port, debug=True)