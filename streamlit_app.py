import streamlit as st
import subprocess
import pyaudio
import requests
import time
import numpy as np

# --- CONFIGURATION ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "ollama_model_name" # Replace with your installed model
RATE_LIMIT_BY_SEC = 0.5

# --- 1. SPEECH INPUT (STT) HANDLERS ---
class VoiceInput:
    def __init__(self):
        self.CHUNK = 1024
        # Initialize PyAudio here or pass it to the function
        self.pa = pyaudio.PyAudio()

    def get_audio_input(self, max_duration_seconds=10):
        """Records audio from the default microphone."""
        stream = self.pa.open(format=pyaudio.paInt16,
                               rate=44100,
                               channels=1,
                               input=True)
        
        print("🎙️ Listening... Speak now.")
        
        audio_data = []
        start_time = time.time()
        while time.time() - start_time < max_duration_seconds:
            data = stream.read(self.CHUNK, exception_on_overflow=False)
            audio_data.append(data)
            
        stream.stop_stream()
        stream.close()
        return audio_data

    def __del__(self):
        self.pa.terminate()

# --- 2. OLLAMA LLM CONNECTION ---
def connect_to_ollama_api(prompt_text: str) -> str:
    """Sends text via the Ollama API and returns the streamed completion."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt_text,
        "stream": True
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
        response.raise_for_status()
        
        full_response = ""
        # Simulate streaming: read chunks and concatenate
        for line in response.iter_lines():
            if line:
                try:
                    data = line.decode('utf-8')
                    # Simple parsing for streamed responses
                    if data:
                        full_response += data
                except UnicodeDecodeError:
                    pass
        return full_response
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama API: {e}"

# --- 3. TEXT TO SPEECH (TTS) HANDLER ---
# NOTE: This placeholder assumes an external TTS service or library (e.g., gTTS, eSpeak)
def speak_response(text: str):
    """Placeholder for Text-to-Speech engine call."""
    print(f"\n🔊 [TTS Playback]: {text[:100]}...")
    # TO_BE_IMPLEMENTED: Use gTTS or similar
    # audio_file_path = generate_audio(text)
    # return audio_file_path