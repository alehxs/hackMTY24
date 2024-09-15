from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import requests


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load API key 
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Function which will encode image
def encodeImage(imagePath):
    with open(imagePath, "rb") as imageFile:
        return base64.b64encode(imageFile.read()).decode('utf-8')
    
@app.route('/upload', methods=['POST'])
def uploadImage():
    
    # Check if image is in image directory
    if 'image' not in request.files:
        return {'error': 'No image provided'}, 400
    
    # Get image path
    image = request.files['image']
    imagePath = os.path.join('uploads', image.filename)
    image.save(imagePath)

    # Getting base64 string
    base64Image = encodeImage(imagePath)

    # Prepare for OpenAPI 
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

    # Send and recieve request to OpenAI
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()

    # Testing
    print("Result before JSON:", result)

    # Return request
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)