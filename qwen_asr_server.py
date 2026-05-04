#!/usr/bin/env python3
"""
Qwen3-ASR Local Server - OpenAI-compatible API for speech recognition
"""

import os
import io
import wave
import struct
import base64
import tempfile
import threading
import time
from flask import Flask, request, jsonify
import torch

# Global model variable
model = None
model_lock = threading.Lock()

def load_model():
    """Load Qwen3-ASR model"""
    global model
    if model is None:
        print("Loading Qwen3-ASR-1.7B model...")
        from qwen_asr import Qwen3ASRModel

        # Check for CUDA
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

        print(f"Using device: {device}, dtype: {dtype}")

        model = Qwen3ASRModel.from_pretrained(
            "Qwen/Qwen3-ASR-1.7B",
            dtype=dtype,
            device_map=device,
            max_inference_batch_size=1,
            max_new_tokens=256,
        )
        print("Model loaded successfully!")
    return model

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"})

@app.route('/v1/audio/transcriptions', methods=['POST'])
def transcribe():
    """OpenAI-compatible transcription endpoint"""
    global model

    try:
        # Get audio file from request
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        audio_file = request.files['file']

        # Debug: check received file
        audio_data = audio_file.read()
        print(f"Received audio file: {len(audio_data)} bytes, filename: {audio_file.filename}")

        # Reset file pointer
        audio_file.seek(0)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            audio_file.save(tmp.name)
            tmp_path = tmp.name

        # Debug: check WAV properties
        import wave
        try:
            with wave.open(tmp_path, 'rb') as wf:
                print(f"WAV properties: {wf.getframerate()}Hz, {wf.getnchannels()} channels, {wf.getsampwidth()*8} bits, {wf.getnframes()} frames")
                duration = wf.getnframes() / wf.getframerate()
                print(f"Audio duration: {duration:.2f} seconds")
        except Exception as e:
            print(f"Failed to read WAV properties: {e}")

        # Get language parameter (optional)
        language = request.form.get('language', None)
        print(f"Language parameter: {language}")

        # Map language codes to Qwen3-ASR language names
        language_map = {
            'zh': 'Chinese',
            'en': 'English',
            'ja': 'Japanese',  # Not in supported list, will be ignored
            'ko': 'Korean',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ar': 'Arabic',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'it': 'Italian',
            'yue': 'Cantonese',
            'multi': None,
            '': None,
        }

        if language in language_map:
            language = language_map[language]
        elif language not in ['Chinese', 'English', 'Cantonese', 'Arabic', 'German', 'French', 'Spanish', 'Portuguese', 'Indonesian', 'Italian', 'Korean', 'Russian', 'Thai', 'Vietnamese', None]:
            # Unsupported language, set to None for auto-detect
            print(f"Unsupported language code: {language}, using auto-detect")
            language = None

        # Transcribe
        with model_lock:
            if model is None:
                load_model()

            results = model.transcribe(
                audio=tmp_path,
                language=language,
            )
            print(f"Transcription result: {results}")

        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass

        # Return result
        if results:
            text = results[0].text
            detected_lang = results[0].language if hasattr(results[0], 'language') else 'unknown'
            print(f"Returning: text='{text}', language='{detected_lang}'")
            return jsonify({"text": text, "language": detected_lang})
        else:
            print("No results returned")
            return jsonify({"text": "", "language": "unknown"})

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/v1/models', methods=['GET'])
def models():
    """List available models"""
    return jsonify({
        "data": [
            {"id": "qwen3-asr-1.7b", "object": "model", "owned_by": "alibaba"}
        ]
    })

def main():
    """Start the server"""
    import argparse

    parser = argparse.ArgumentParser(description='Qwen3-ASR Local Server')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host address')
    parser.add_argument('--port', type=int, default=8801, help='Port number')
    parser.add_argument('--preload', action='store_true', help='Preload model on startup')

    args = parser.parse_args()

    # Preload model if requested
    if args.preload:
        load_model()

    print(f"Starting Qwen3-ASR server on {args.host}:{args.port}")
    print("Press Ctrl+C to stop")

    app.run(host=args.host, port=args.port, threaded=True)

if __name__ == '__main__':
    main()