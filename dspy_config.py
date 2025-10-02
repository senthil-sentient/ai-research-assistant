#!/usr/bin/env python3
"""
DSPy configuration helper for serverless deployments like Vercel.
This module ensures DSPy works correctly in environments with restricted filesystem access.
"""

import os
import tempfile

def configure_dspy_for_serverless():
    """
    Configure DSPy to work in serverless environments by setting up
    a writable cache directory.
    
    This should be called before importing DSPy in any module.
    """
    # Set cache directory to /tmp which is writable in serverless environments
    cache_dir = os.environ.get('DSPY_CACHE_DIR', '/tmp/.dspy_cache')
    
    try:
        # Ensure the cache directory exists and is writable
        os.makedirs(cache_dir, exist_ok=True)
        os.environ['DSPY_CACHE_DIR'] = cache_dir
        
        # Test write access
        test_file = os.path.join(cache_dir, 'test_write.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        
        print(f"✅ DSPy cache configured: {cache_dir}")
        return True
        
    except Exception as e:
        print(f"⚠️  Warning: Could not configure DSPy cache directory: {e}")
        print("   DSPy may still work but caching will be disabled")
        return False

def get_dspy_lm(api_key: str = None):
    """
    Get a configured DSPy LM instance.
    
    Args:
        api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable.
    
    Returns:
        Configured dspy.LM instance
    """
    # Import DSPy after configuration
    import dspy
    
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
    
    lm = dspy.LM("openai/gpt-4o-mini", api_key=api_key)
    dspy.configure(lm=lm)
    return lm

def get_dspy_lm_if_available():
    """
    Get a configured DSPy LM instance if API key is available, otherwise return None.
    This is useful for testing or when API key might not be available.
    
    Returns:
        Configured dspy.LM instance or None
    """
    try:
        return get_dspy_lm()
    except ValueError:
        return None

# Auto-configure when this module is imported
configure_dspy_for_serverless()
