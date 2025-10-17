# Vercel API Routes for Cognivasc Backend
# This file allows deploying the FastAPI backend as Vercel serverless functions

import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import the FastAPI app
from app import app

# Export the app for Vercel
handler = app
