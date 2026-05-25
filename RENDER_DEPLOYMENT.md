# Render Deployment Guide

This project is ready to deploy as a Render Web Service. You do not need to buy a domain; Render gives the service a free `onrender.com` HTTPS URL.

## What Render Uses

The root `render.yaml` defines the web service:

- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn web_app:app --host 0.0.0.0 --port $PORT`
- Health check: `/api/health`
- Plan: free

## Required Environment Variables

Add these in Render during setup. Do not commit real values to GitHub.

```env
DATABASE_URL=your_supabase_connection_string
GROQ_API_KEY=your_groq_api_key
WEB_SINGLE_USER_ID=your_numeric_telegram_user_id
WEB_ACCESS_KEY=a_long_private_random_value
ENV=production
```

`WEB_SINGLE_USER_ID` should be the same numeric Telegram user id that already has your progress in the database.

`WEB_ACCESS_KEY` is the private key in your personal URL. Anyone with this key can use the app, so keep it private.

## Deploy Steps

1. Push this branch to GitHub.
2. Open the Render Dashboard.
3. Click **New** > **Blueprint**.
4. Connect `mayurrajBhor/custom-aptitude-practice-bot`.
5. Render should detect `render.yaml`.
6. Enter the required environment variables when Render asks for them.
7. Deploy the Blueprint.

After deployment, Render gives you a URL like:

```text
https://custom-aptitude-practice-bot.onrender.com
```

Open this private URL once on every device:

```text
https://custom-aptitude-practice-bot.onrender.com/?key=your_WEB_ACCESS_KEY
```

After the first visit, the browser stores the key locally, and the app syncs the same progress through Supabase.

## If You Use Manual Web Service Setup Instead

Choose **New** > **Web Service**, connect the GitHub repo, then use:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn web_app:app --host 0.0.0.0 --port $PORT
Health Check Path: /api/health
```

Then add the same environment variables listed above.

## Telegram Bot Worker

The web app works without Telegram. If you later want Telegram commands and smart Telegram reminders running on Render too, create a separate Background Worker with:

```text
Build Command: pip install -r requirements.txt
Start Command: python bot.py
```

That worker also needs:

```env
TELEGRAM_BOT_TOKEN=your_production_bot_token
DATABASE_URL=your_supabase_connection_string
GROQ_API_KEY=your_groq_api_key
WEB_APP_URL=https://custom-aptitude-practice-bot.onrender.com/?key=your_WEB_ACCESS_KEY
ENV=production
```

For the first web deployment, skip the worker unless you specifically need Telegram running from Render.
