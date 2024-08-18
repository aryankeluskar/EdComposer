import requests

import os
from dotenv import load_dotenv

load_dotenv()


async def generate_voice(sentence, index):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/j9jfwdrw7BRfcR43Qohk"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
    }

    data = {
        "text": str(sentence),
        "model_id": "eleven_turbo_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    response = requests.post(url, json=data, headers=headers)
    print(response.text)
    with open(f"output_{index}.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
        print("saved file")
