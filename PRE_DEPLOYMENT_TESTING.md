# Pre-Deployment Testing Guide

This guide provides comprehensive testing procedures to ensure your AI Research Assistant is ready for Vercel deployment.

## Quick Start

Run the automated test suite:
```bash
python test_build.py
```

## Manual Testing Checklist

### 1. Environment Setup

Before testing, ensure you have:
- [ ] Python 3.8+ installed
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] OpenAI API key available (for full testing)

### 2. Local Testing

#### Basic Functionality Test
```bash
# Set environment variables
export OPENAI_API_KEY="your-api-key-here"
export SECRET_KEY="your-secret-key-here"

# Run the application
python app.py

# In another terminal, test endpoints
curl http://localhost:8080/api/health
curl http://localhost:8080/
```

#### Full Integration Test
```bash
# Test with actual API calls
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "urls": ["https://en.wikipedia.org/wiki/Machine_learning"],
    "reasoning_approach": "cot"
  }'
```

### 3. Vercel-Specific Testing

#### Build Simulation
```bash
# Test that the app can be imported in a clean environment
python -c "
import os
os.environ['OPENAI_API_KEY'] = 'test'
from app import app
print('✅ Build simulation successful')
"
```

#### Configuration Validation
- [ ] `vercel.json` exists and is valid JSON
- [ ] `app.py` is specified as the source in builds
- [ ] Routes are properly configured
- [ ] All required files are present

### 4. Dependency Testing

#### Check for Conflicts
```bash
# Check for known version conflicts
python -c "
import openai
import langchain_openai
print(f'OpenAI: {openai.__version__}')
print(f'LangChain OpenAI: {langchain_openai.__version__}')
"
```

#### Verify All Requirements
```bash
# Test each requirement individually
python -c "
import dspy
import flask
import requests
import beautifulsoup4
print('✅ All core dependencies available')
"
```

### 5. File Structure Validation

Ensure these files exist:
- [ ] `app.py` - Main Flask application
- [ ] `test_dspy.py` - Core research system
- [ ] `dspy_config.py` - DSPy configuration
- [ ] `requirements.txt` - Python dependencies
- [ ] `vercel.json` - Vercel configuration
- [ ] `templates/index.html` - Frontend template
- [ ] `package.json` - Node.js configuration (optional)

### 6. API Endpoint Testing

Test all endpoints:
- [ ] `GET /` - Main page loads
- [ ] `GET /api/health` - Health check returns 200
- [ ] `POST /api/chat` - Chat endpoint handles requests
- [ ] `GET /api/chat/history` - Chat history endpoint
- [ ] `POST /api/chat/clear` - Clear chat history

### 7. Error Handling Testing

Test error scenarios:
- [ ] Missing API key handling
- [ ] Invalid request data
- [ ] Network timeouts
- [ ] Invalid URLs in research requests

## Automated Testing

### Using the Test Script

The `test_build.py` script provides comprehensive automated testing:

```bash
# Run all tests
python test_build.py

# Run specific test (modify script for individual tests)
python -c "
from test_build import test_flask_app
test_flask_app()
"
```

### Test Categories

1. **File Structure Test** - Verifies all required files exist
2. **Requirements Test** - Checks all dependencies are installed
3. **Import Test** - Tests module imports work correctly
4. **Flask App Test** - Tests Flask application functionality
5. **Vercel Config Test** - Validates Vercel configuration
6. **Dependencies Test** - Checks for version conflicts
7. **Build Simulation Test** - Simulates Vercel build process

## Common Issues and Solutions

### Issue: OpenAI API Key Required
**Solution**: Set environment variable before testing
```bash
export OPENAI_API_KEY="your-key-here"
```

### Issue: Missing Dependencies
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: Import Errors
**Solution**: Check Python path and virtual environment
```bash
which python
pip list | grep dspy
```

### Issue: Flask App Won't Start
**Solution**: Check port availability and configuration
```bash
lsof -i :8080  # Check if port is in use
```

## Pre-Deployment Checklist

Before deploying to Vercel:

- [ ] All automated tests pass (`python test_build.py`)
- [ ] Local testing completed successfully
- [ ] Environment variables configured in Vercel dashboard
- [ ] No critical warnings in test output
- [ ] All required files committed to Git
- [ ] `vercel.json` configuration validated

## Vercel Deployment Commands

### Using Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Using Git Integration
1. Push code to your Git repository
2. Connect repository in Vercel dashboard
3. Configure environment variables
4. Deploy

## Environment Variables for Vercel

Set these in your Vercel dashboard:
- `OPENAI_API_KEY` - Your OpenAI API key
- `SECRET_KEY` - Flask secret key (optional)

## Monitoring After Deployment

After deployment, monitor:
- [ ] Application logs in Vercel dashboard
- [ ] Function execution times
- [ ] Error rates
- [ ] API response times

## Troubleshooting

### Build Failures
1. Check Vercel build logs
2. Verify all dependencies in `requirements.txt`
3. Test locally with same Python version
4. Check for import errors

### Runtime Errors
1. Check environment variables
2. Review application logs
3. Test API endpoints individually
4. Verify external service connectivity

### Performance Issues
1. Monitor function execution time
2. Check for memory leaks
3. Optimize imports and dependencies
4. Consider caching strategies

## Success Criteria

Your deployment is ready when:
- ✅ All automated tests pass
- ✅ Local testing successful
- ✅ No critical errors in logs
- ✅ All endpoints responding correctly
- ✅ Environment variables configured
- ✅ Performance within acceptable limits

---

**Remember**: Always test thoroughly before deploying to production. The automated test script (`test_build.py`) should be your first step in the deployment process.
