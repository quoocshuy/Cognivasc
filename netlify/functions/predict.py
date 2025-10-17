# Netlify Function for Cognivasc Prediction API
import json
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

def handler(event, context):
    """Netlify function handler for prediction API"""

    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }

    # Handle preflight requests
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    try:
        # Import prediction logic
        from app import run_prediction
        from PIL import Image
        import io
        import base64

        # Parse request body
        body = json.loads(event['body'])

        # Decode base64 image
        image_data = base64.b64decode(body['image'])
        img = Image.open(io.BytesIO(image_data))

        # Run prediction
        result = run_prediction(img)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
