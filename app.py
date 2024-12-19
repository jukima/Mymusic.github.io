from flask import Flask, request, jsonify, send_file
import os
import youtube_dl

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_music():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'message': 'No URL provided'}), 400

    try:
        # Set download options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        # Download the audio
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        return jsonify({'success': True, 'file': f'/file/{os.path.basename(filename)}'})

    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Failed to download'}), 500

@app.route('/file/<filename>', methods=['GET'])
def serve_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)