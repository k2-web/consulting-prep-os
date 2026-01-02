# Deployment Guide: AlphaOne Due Diligence Platform

This guide explains how to deploy the AlphaOne platform so you can share it with others via a link.

## 1. Important Note on Real-Time Data

The platform currently uses a local Python script (`fetch_market_data.py`) to fetch live stock prices from Yahoo Finance.
**When you deploy this as a static website (e.g., on Netlify or Vercel), this Python script will NOT run automatically.**

### What this means for the shared link

- The "Live Prices" will default to the last snapshot you generated locally (stored in `live_data.js`).
- The "Jitter" effect (simulated price movement) **WILL** still work, so the site will feel alive and interactive.
- Users can search for tickers, but if the data isn't in `live_data.js`, it will generate realistic mock data.

## 2. Deployment Options

### Option A: Netlify Drop (Easiest)

1. Locate the `slide_deck` folder on your computer:
    `/Users/kunsh/.gemini/antigravity/playground/blazing-mare/slide_deck`
2. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
3. Drag and drop the `slide_deck` folder onto the page.
4. Netlify will instantly deploy it and give you a shareable URL (e.g., `https://alphaone-demo.netlify.app`).

### Option B: GitHub Pages (Best for Updates)

1. Create a new repository on GitHub.
2. Upload the contents of the `slide_deck` folder to the repository.
3. Go to **Settings** > **Pages**.
4. Select the `main` branch and click **Save**.
5. GitHub will provide a link (e.g., `https://yourusername.github.io/repo-name`).

## 3. Updating Data

To update the "Live Prices" on your shared site:

1. Run the Python script locally:

    ```bash
    python3 fetch_market_data.py
    ```

2. This updates `live_data.js`.
3. Re-deploy the `slide_deck` folder (or push changes to GitHub).
