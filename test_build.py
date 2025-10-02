#!/usr/bin/env python3
"""
Pre-deployment testing script for Vercel deployment
Run this before deploying to ensure everything works correctly
"""

import os
import sys
import subprocess
import requests
import time
import json
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    try:
        # Set test environment first
        os.environ['OPENAI_API_KEY'] = 'test_key_for_import_test'
        
        # Test core imports
        from dspy_config import configure_dspy_for_serverless
        configure_dspy_for_serverless()
        from test_dspy import DeepResearchSystem
        from app import app
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_requirements():
    """Test that all requirements are properly installed"""
    print("🔍 Testing requirements...")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        # Package name mapping for imports
        package_mapping = {
            'dspy-ai': 'dspy',
            'markdown-it-py': 'markdown_it',
            'python-dotenv': 'dotenv',
            'beautifulsoup4': 'bs4',
            'pyyaml': 'yaml',
            'rpds-py': 'rpds',
        }
        
        missing_packages = []
        for req in requirements:
            if req.strip() and not req.startswith('#'):
                package_name = req.split('==')[0].split('>=')[0].split('<=')[0]
                import_name = package_mapping.get(package_name, package_name.replace('-', '_'))
                try:
                    __import__(import_name)
                except ImportError:
                    missing_packages.append(package_name)
        
        if missing_packages:
            print(f"❌ Missing packages: {missing_packages}")
            return False
        else:
            print("✅ All requirements satisfied")
            return True
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        return False

def test_flask_app():
    """Test Flask app initialization and basic endpoints"""
    print("🔍 Testing Flask app...")
    try:
        # Set test environment
        os.environ['OPENAI_API_KEY'] = 'test_key_for_build_test'
        os.environ['SECRET_KEY'] = 'test_secret_key'
        
        from app import app
        
        # Test app creation
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
            
            # Test main page
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Main page loads")
            else:
                print(f"❌ Main page failed: {response.status_code}")
                return False
            
            # Test chat endpoint with invalid data (should return 400)
            response = client.post('/api/chat', 
                                 json={'question': '', 'urls': []},
                                 content_type='application/json')
            if response.status_code == 400:
                print("✅ Chat endpoint validation working")
            else:
                print(f"❌ Chat endpoint validation failed: {response.status_code}")
                return False
        
        print("✅ Flask app tests passed")
        return True
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_vercel_config():
    """Test Vercel configuration"""
    print("🔍 Testing Vercel configuration...")
    try:
        # Check vercel.json exists and is valid
        if not Path('vercel.json').exists():
            print("❌ vercel.json not found")
            return False
        
        with open('vercel.json', 'r') as f:
            config = json.load(f)
        
        # Validate required fields
        required_fields = ['version', 'builds', 'routes']
        for field in required_fields:
            if field not in config:
                print(f"❌ Missing required field in vercel.json: {field}")
                return False
        
        # Check that app.py is specified as source
        builds = config.get('builds', [])
        if not any(build.get('src') == 'app.py' for build in builds):
            print("❌ app.py not found in builds configuration")
            return False
        
        print("✅ Vercel configuration valid")
        return True
    except Exception as e:
        print(f"❌ Vercel config test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing file structure...")
    required_files = [
        'app.py',
        'test_dspy.py',
        'dspy_config.py',
        'requirements.txt',
        'vercel.json',
        'templates/index.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def test_dependencies_compatibility():
    """Test for common dependency conflicts"""
    print("🔍 Testing dependency compatibility...")
    try:
        # Check for known conflicts
        import openai
        import langchain_openai
        
        # Check versions
        openai_version = openai.__version__
        if openai_version.startswith('2.'):
            print("⚠️  Warning: OpenAI 2.x detected, may conflict with langchain-openai")
        
        print("✅ Dependency compatibility check completed")
        return True
    except ImportError as e:
        print(f"⚠️  Warning: Could not check all dependencies: {e}")
        return True  # Not critical for build
    except Exception as e:
        print(f"❌ Dependency check failed: {e}")
        return False

def test_vercel_build_simulation():
    """Simulate Vercel build process"""
    print("🔍 Simulating Vercel build...")
    try:
        # Test that the app can be imported in a clean environment
        # This simulates what Vercel does
        env = os.environ.copy()
        env['OPENAI_API_KEY'] = 'test_key'
        env['SECRET_KEY'] = 'test_secret'
        
        # Test import in subprocess (simulates Vercel's clean environment)
        result = subprocess.run([
            sys.executable, '-c', 
            'import os; os.environ["OPENAI_API_KEY"]="test"; from app import app; print("Build simulation successful")'
        ], env=env, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Vercel build simulation successful")
            return True
        else:
            print(f"❌ Vercel build simulation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Vercel build simulation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting pre-deployment tests...\n")
    
    tests = [
        ("File Structure", test_file_structure),
        ("Requirements", test_requirements),
        ("Imports", test_imports),
        ("Flask App", test_flask_app),
        ("Vercel Config", test_vercel_config),
        ("Dependencies", test_dependencies_compatibility),
        ("Vercel Build Simulation", test_vercel_build_simulation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for Vercel deployment.")
        return 0
    else:
        print("❌ Some tests failed. Fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
