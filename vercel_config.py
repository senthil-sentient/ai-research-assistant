#!/usr/bin/env python3
"""
Vercel-specific configuration that must be imported first.
This sets up the environment for serverless deployment.
"""

import os

# Set DSPy cache directory to /tmp which is writable in Vercel
os.environ['DSPY_CACHE'] = '/tmp/.dspy_cache'

# Ensure the cache directory exists
try:
    os.makedirs('/tmp/.dspy_cache', exist_ok=True)
except Exception:
    pass  # Directory might already exist or creation might fail

# Set other serverless-friendly environment variables
os.environ['DSPY_DISABLE_CACHE'] = '0'  # Keep cache but use /tmp
os.environ['TMPDIR'] = '/tmp'  # Set temp directory

print("✅ Vercel environment configured")
