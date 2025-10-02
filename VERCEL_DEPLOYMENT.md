# Vercel Deployment Guide

This guide will help you deploy your AI Research Assistant to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Your OpenAI API key
3. Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### 1. Prepare Your Repository

Make sure all the following files are in your repository root:

```
├── app.py                 # Flask application
├── test_dspy.py          # Core research system
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── package.json         # Node.js configuration
└── templates/
    └── index.html       # Web interface
```

### 2. Deploy to Vercel

#### Option A: Deploy via Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from your project directory:
   ```bash
   vercel
   ```

4. Follow the prompts:
   - Set up and deploy? **Yes**
   - Which scope? **Your account**
   - Link to existing project? **No**
   - Project name: **ai-research-assistant** (or your preferred name)
   - Directory: **./** (current directory)
   - Override settings? **No**

#### Option B: Deploy via Vercel Dashboard

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Vercel will automatically detect it's a Python project
5. Configure environment variables (see step 3)
6. Click "Deploy"

### 3. Configure Environment Variables

In your Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variable:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key
   - **Environment**: Production, Preview, Development

### 4. Test Your Deployment

1. Visit your deployed URL (provided by Vercel)
2. Enter your OpenAI API key in the sidebar
3. Test with a sample research question and URLs

## Features

Your deployed application includes:

- **Web Interface**: Clean, responsive design similar to ChatGPT
- **Flexible Reasoning**: Choose between Chain of Thought and ReAct approaches
- **Real-time Research**: Conduct research on multiple URLs simultaneously
- **Chat History**: Persistent chat sessions
- **Source Attribution**: See which sources were used for each answer
- **Mobile Responsive**: Works on desktop and mobile devices

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `SECRET_KEY`: Flask secret key (optional, auto-generated if not provided)

### Customization

You can customize the application by modifying:

- `templates/index.html`: Frontend interface and styling
- `app.py`: Backend API endpoints and logic
- `test_dspy.py`: Core research functionality

## Troubleshooting

### Common Issues

1. **"Module not found" errors**: Ensure all dependencies are in `requirements.txt`
2. **API key not working**: Verify the environment variable is set correctly
3. **Research fails**: Check that URLs are accessible and valid
4. **Styling issues**: Clear browser cache and check console for errors

### Debug Mode

To run locally for debugging:

```bash
pip install -r requirements.txt
python app.py
```

Then visit `http://localhost:5000`

### Vercel Logs

Check deployment logs in your Vercel dashboard:
1. Go to your project
2. Click "Functions" tab
3. View logs for any errors

## Scaling

Vercel automatically handles:
- **Serverless scaling**: Functions scale based on demand
- **Global CDN**: Fast loading worldwide
- **Auto-deployments**: Deploy on every Git push

## Security Notes

- Never commit your OpenAI API key to Git
- Use environment variables for sensitive data
- The application uses session-based storage (not persistent database)
- Consider adding authentication for production use

## Support

If you encounter issues:

1. Check the Vercel documentation
2. Review the application logs
3. Test locally first
4. Ensure all dependencies are compatible

## Next Steps

After successful deployment, you can:

1. Set up custom domain
2. Configure analytics
3. Add authentication
4. Implement database storage for chat history
5. Add more reasoning approaches
6. Integrate with other AI models

---

**Happy Researching! 🔍**
