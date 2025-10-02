#!/bin/bash

# Pre-deployment and deployment script for Vercel
# Usage: ./deploy.sh [--skip-tests] [--prod]

set -e  # Exit on any error

echo "🚀 Starting deployment process..."

# Parse arguments
SKIP_TESTS=false
PROD_DEPLOY=false

for arg in "$@"; do
    case $arg in
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --prod)
            PROD_DEPLOY=true
            shift
            ;;
        *)
            echo "Unknown option: $arg"
            echo "Usage: $0 [--skip-tests] [--prod]"
            exit 1
            ;;
    esac
done

# Step 1: Run tests (unless skipped)
if [ "$SKIP_TESTS" = false ]; then
    echo "🔍 Running pre-deployment tests..."
    python test_build.py
    if [ $? -ne 0 ]; then
        echo "❌ Tests failed. Aborting deployment."
        exit 1
    fi
    echo "✅ All tests passed!"
else
    echo "⚠️  Skipping tests (--skip-tests flag used)"
fi

# Step 2: Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Step 3: Check if logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please log in to Vercel..."
    vercel login
fi

# Step 4: Deploy
echo "🚀 Deploying to Vercel..."
if [ "$PROD_DEPLOY" = true ]; then
    echo "📤 Deploying to production..."
    vercel --prod
else
    echo "📤 Deploying to preview..."
    vercel
fi

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Check your deployment URL in the output above"
echo "2. Test the deployed application"
echo "3. Configure environment variables in Vercel dashboard if needed"
echo "4. Monitor logs in Vercel dashboard"
