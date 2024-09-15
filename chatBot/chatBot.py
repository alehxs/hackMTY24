from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import requests

# Load API key
load_dotenv()

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Function which will encode image
def encodeImage(imagePath):
    with open(imagePath, "rb") as imageFile:
        return base64.b64encode(imageFile.read()).decode('utf-8')
    
# Path to users image
#imagePath = "TestDamageConstruction.jpeg"
imagePath = "HorseDemo.jpg"

# Getting base64 string
base64Image = encodeImage(imagePath)


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OpenAI.api_key}"
}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What physical damages appear in this image if any? If none respond with 'No visible damages. Could require further inspection.'"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64Image}"
                    }
                }
            ]
        }
    ],
    "max_tokens": 200
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())