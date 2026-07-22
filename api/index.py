import sys
import os

# Add the project root (one level up from /api) to the path so we can import app.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import app  # noqa: E402

# Vercel's Python runtime detects and serves this WSGI app automatically
