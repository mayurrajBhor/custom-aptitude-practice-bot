# Personal Web Access

The browser app can run as a single-user website without a login screen.

Set these environment variables on the hosting service:

```env
WEB_SINGLE_USER_ID=your_telegram_numeric_user_id
WEB_ACCESS_KEY=a_long_private_random_value
```

Use the private link once on each device. With Render, this will look like:

```text
https://your-render-service.onrender.com/?key=a_long_private_random_value
```

After the first visit, the browser stores the private key locally and the app keeps using the same `WEB_SINGLE_USER_ID`, so progress, mistakes, unlocks, and reminders stay synced through the database.

Security notes:

- `WEB_SINGLE_USER_ID` must be the same numeric user id used by your Telegram bot progress.
- `WEB_ACCESS_KEY` is not a full login system. Anyone with the private link can use the app.
- Do not put real API keys in GitHub. Store them only in the hosting provider's environment/secrets settings.

See `RENDER_DEPLOYMENT.md` for the full Render setup.
