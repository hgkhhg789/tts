import asyncio
import os
import time
from flask import Blueprint, request, jsonify
from edge_tts import Communicate

# Define Flask Blueprint for TTS API
tts_bp = Blueprint('tts', __name__)

VALID_VOICES = ["vi-VN-HoaiMyNeural", "vi-VN-NamMinhNeural"]

# Directory configuration (matching app.py)
MEDIA_FOLDER = 'media'
SHORT_MEDIA_FOLDER = os.path.join(MEDIA_FOLDER, 'short')
LONG_MEDIA_FOLDER = os.path.join(MEDIA_FOLDER, 'long')

# Ensure directories exist
os.makedirs(SHORT_MEDIA_FOLDER, exist_ok=True)
os.makedirs(LONG_MEDIA_FOLDER, exist_ok=True)

# Async TTS function
async def text_to_speech(text, voice, output_file):
    if voice not in VALID_VOICES:
        voice = "vi-VN-HoaiMyNeural"
    tts = Communicate(text, voice)
    await tts.save(output_file)

# Sync wrapper for TTS
def run_tts(input_text, voice, save_path):
    asyncio.run(text_to_speech(input_text, voice, save_path))

# API endpoint for short-term storage
@tts_bp.route('/api/short', methods=['POST'])
def tts_short():
    text = request.form.get('text')
    voice = request.form.get('voice', "vi-VN-HoaiMyNeural")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    filename = f"short_{int(time.time())}.mp3"
    file_path = os.path.join(SHORT_MEDIA_FOLDER, filename)
    
    run_tts(text, voice, file_path)
    
    return jsonify({"message": "File saved", "audioUrl": f"/media/short/{filename}"}), 200

# API endpoint for long-term storage
@tts_bp.route('/api/long', methods=['POST'])
def tts_long():
    text = request.form.get('text')
    voice = request.form.get('voice', "vi-VN-HoaiMyNeural")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    filename = f"long_{int(time.time())}.mp3"
    file_path = os.path.join(LONG_MEDIA_FOLDER, filename)
    
    run_tts(text, voice, file_path)
    
    return jsonify({"message": "File saved", "audioUrl": f"/media/long/{filename}"}), 200