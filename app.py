from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        output_file = 'audio.mp3'
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_file,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

if __name__ == '__main__':
    app.run(debug=True)
