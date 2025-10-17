# Vercel API Handler for Cognivasc Backend
import json
import base64
import io
from pathlib import Path
import sys

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import FastAPI app
from app import app

def handler(request):
    """Vercel serverless function handler"""

    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }

    # Handle preflight requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    try:
        # Route requests to FastAPI app
        if request.path == '/health':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'status': 'healthy'})
            }

        elif request.path == '/predict':
            # Handle prediction request
            body = json.loads(request.body) if request.body else {}

            if 'image' not in body:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'No image provided'})
                }

            # Decode base64 image
            image_data = base64.b64decode(body['image'])

            # Import prediction function
            from app import run_prediction
            from PIL import Image

            img = Image.open(io.BytesIO(image_data))
            result = run_prediction(img)

            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(result)
            }

        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
