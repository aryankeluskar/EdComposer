import requests
import dotenv
import os

dotenv.load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/warp-ai/wuerstchen"
headers = {"Authorization": "Bearer " + os.getenv("HUGGING_FACE_MODEL")}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


image_bytes = query(
    {
        "inputs": "a white siamese cat. powerpoint presentation clipart style",
    }
)

with open("image.jpg", "wb") as f:
    f.write(image_bytes)
