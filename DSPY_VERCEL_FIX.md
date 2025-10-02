# DSPy Vercel Deployment Fix

## Problem
The DSPy library was failing to deploy on Vercel with the following error:
```
OSError: [Errno 30] Cache directory "/home/sbx_user1051/.dspy_cache/000" does not exist and could not be created
```

## Root Cause
DSPy tries to create a cache directory in the user's home directory (`~/.dspy_cache/`), but Vercel's serverless environment has restricted filesystem access and cannot create directories in the home directory.

## Solution
Created a `dspy_config.py` module that:

1. **Sets up a writable cache directory**: Configures DSPy to use `/tmp/.dspy_cache` instead of the home directory
2. **Ensures directory exists**: Creates the cache directory before DSPy initialization
3. **Provides helper functions**: Offers `get_dspy_lm()` and `get_dspy_lm_if_available()` for easy DSPy configuration
4. **Auto-configures on import**: Sets up the environment automatically when the module is imported

## Files Modified

### `dspy_config.py` (new)
- Centralized DSPy configuration for serverless environments
- Handles cache directory setup and API key management
- Provides robust error handling

### `test_dspy.py`
- Updated to use `dspy_config.get_dspy_lm()` instead of direct DSPy configuration
- Ensures cache directory is set before DSPy import

### `advanced_research_system.py`
- Updated to use `dspy_config.get_dspy_lm()` instead of direct DSPy configuration
- Ensures cache directory is set before DSPy import

## Usage
The fix is automatic - no changes needed in your application code. Simply import from the existing modules:

```python
from test_dspy import DeepResearchSystem
from advanced_research_system import OptimizedResearchSystem
```

## Environment Variables
Make sure to set the following environment variable in Vercel:
- `OPENAI_API_KEY`: Your OpenAI API key

## Testing
The configuration has been tested locally and should work correctly in the Vercel serverless environment. The `/tmp` directory is writable in Vercel's runtime, making it suitable for DSPy's cache requirements.
