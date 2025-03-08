from flask import Flask, Response, request, jsonify
from yt_dlp import YoutubeDL
import os
import json

app = Flask(__name__)

@app.route('/api/search', methods=['GET'])
def search_video():
    url = request.args.get('url', '')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        with YoutubeDL({
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "title": info.get('title', ''),
                "thumbnail": info.get('thumbnail', ''),
                "duration": info.get('duration', 0),
                "uploader": info.get('uploader', '')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download_video():
    url = request.args.get('url', '')
    format = request.args.get('format', 'mp4')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
            
            # Redirige al usuario directamente al archivo de video
            # (Esta es una simplificación - no convierte a AVI)
            return jsonify({
                "direct_url": video_url,
                "title": info.get('title', '')
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Esto es solo para desarrollo local
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)