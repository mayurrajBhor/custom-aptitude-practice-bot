# Supabase Database Restoration Guide 🛠️

If you want to use **Supabase only** and skip the local SQLite fallback, follow these steps to fix your connection.

## 1. Verify Project Status 🔍
The error `Tenant or user not found` almost always means one of two things:
- **Project is Paused**: Free tier projects are paused after 1 week of inactivity. Log into [Supabase Dashboard](https://supabase.com/dashboard) and click **"Restore Project"**.
- **Incorrect Project ID**: Your current project ID is `dfqimwamzsnrfnpnvvvd`. If you deleted that project and made a new one, you MUST update your `.env` file.

## 2. Find Your Connection String 🔑
In your Supabase Dashboard:
1.  Go to **Project Settings** > **Database**.
2.  Scroll down to **Connection string**.
3.  Copy the **URI** (ensure you select "Transaction" mode/port 6543 for better stability).
4.  Replace the `DATABASE_URL` in your `.env` file with this new string.

## 3. Verify Local Connection ⚡
Once you've updated your `.env`, run this command to test it:
```bash
python tmp/db_check.py
```

---
> [!IMPORTANT]
> I have removed the SQLite fallback logic as requested. The bot will now wait for a valid Supabase connection to start. 
