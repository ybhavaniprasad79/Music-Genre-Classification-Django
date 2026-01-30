# Deploy to Render.com - Step by Step Guide

## Prerequisites
- GitHub account
- Render.com account (free - sign up at https://render.com)

## Step 1: Push Your Code to GitHub

1. **Initialize Git (if not already done):**
   ```bash
   cd /home/tony/projects/Music-Genre-Classification-Django
   git init
   git add .
   git commit -m "Prepare for Render deployment"
   ```

2. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name it: `music-genre-classifier` (or any name you like)
   - Don't initialize with README (you already have code)
   - Click "Create repository"

3. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/music-genre-classifier.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Set Up on Render.com

1. **Sign up/Login to Render:**
   - Go to https://render.com
   - Sign up with GitHub (recommended)

2. **Create a New Web Service:**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account if not already connected
   - Select your repository: `music-genre-classifier`

3. **Configure the Web Service:**

   **Basic Settings:**
   - **Name:** `music-genre-classifier` (or your choice)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** (leave blank)
   - **Runtime:** `Python 3`

   **Build & Deploy:**
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn MusicClassification.wsgi:application`

4. **Environment Variables:**
   Click "Advanced" → Add these environment variables:

   | Key | Value |
   |-----|-------|
   | `PYTHON_VERSION` | `3.12.3` |
   | `SECRET_KEY` | Generate a new one (see below) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-app-name.onrender.com` |

   **Generate a SECRET_KEY:**
   Run this locally:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the output and use it as SECRET_KEY

5. **Create the Web Service:**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment (first time takes longer)

## Step 3: After Deployment

1. **Check the deployment:**
   - Once status shows "Live", click on your app URL
   - It will be: `https://your-app-name.onrender.com`

2. **If there are errors:**
   - Check logs in Render dashboard
   - Common issues:
     - Missing dependencies → check requirements.txt
     - Static files not loading → run collectstatic
     - Database errors → migrations didn't run

## Step 4: Update ALLOWED_HOSTS

After you get your Render URL, update the environment variable:
- Go to Render dashboard → Your service → Environment
- Update `ALLOWED_HOSTS` to: `your-actual-app-name.onrender.com`
- Save changes (auto-redeploys)

## Important Notes:

### Free Tier Limitations:
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 750 hours/month free (enough for one service)

### Future Updates:
When you make code changes:
```bash
git add .
git commit -m "Your update message"
git push origin main
```
Render will auto-deploy!

### Database (Optional):
For production, consider PostgreSQL:
- Render → New → PostgreSQL
- Connect it via DATABASE_URL environment variable
- Update settings.py to use it

## Troubleshooting:

**Build fails:**
- Check Python version compatibility
- Verify all dependencies in requirements.txt

**500 errors:**
- Check logs in Render dashboard
- Ensure DEBUG=False
- Check ALLOWED_HOSTS includes your domain

**Static files missing:**
- Verify WhiteNoise is installed
- Check build.sh runs collectstatic
- Ensure STATIC_ROOT is set

**App runs but features don't work:**
- Large file uploads may timeout (adjust in Render settings)
- Audio processing is CPU-intensive (may be slow on free tier)

## Your app is ready! 🎉

Access it at: `https://your-app-name.onrender.com`
