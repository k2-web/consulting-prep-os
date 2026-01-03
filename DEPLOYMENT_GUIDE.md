# Deployment Guide: Consulting Prep OS

This guide will help you deploy your **Consulting Prep Web App** to the internet using **Streamlit Cloud** so you can share it with others.

## Prerequisites

1. **GitHub Account**: You need a free account at [github.com](https://github.com).
2. **Streamlit Account**: You need a free account at [share.streamlit.io](https://share.streamlit.io) (sign up with your GitHub account).

## Step 1: Upload Code to GitHub

Streamlit Cloud runs apps directly from a GitHub repository.

1. **Create a New Repository**:
    * Go to GitHub and click the **+** icon -> **New repository**.
    * Name it `consulting-prep-os`.
    * Select **Public**.
    * Click **Create repository**.

2. **Upload Files**:
    * If you are familiar with `git` command line:

        ```bash
        git init
        git add .
        git commit -m "Initial commit"
        git branch -M main
        git remote add origin https://github.com/YOUR_USERNAME/consulting-prep-os.git
        git push -u origin main
        ```

    * **Easier Method (Web Upload)**:
        * In your new repository page, click **uploading an existing file**.
        * Drag and drop ALL files from your `consulting-prep` folder (including `Home.py`, `pages/`, `content/`, `utils.py`, `backend.py`, `requirements.txt`, `.streamlit/`).
        * **Important**: Ensure `requirements.txt` is in the root or same folder as `Home.py`.
        * Click **Commit changes**.

## Step 2: Deploy on Streamlit Cloud

1. **Log in to Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io).
2. **New App**: Click the **New app** button.
3. **Select Repository**:
    * **Repository**: Select `YOUR_USERNAME/consulting-prep-os`.
    * **Branch**: `main`.
    * **Main file path**: `consulting-prep/Home.py` (CRITICAL: Do not leave this as default `streamlit_app.py`).
4. **Deploy**: Click **Deploy!**

## Step 3: Verify & Share

* Streamlit will take a minute to install dependencies (from `requirements.txt`) and boot up the app.
* Once live, you will get a URL like `https://consulting-prep-os.streamlit.app`.
* **Share this URL** with Tanvi or anyone else!

## Troubleshooting

* **"Module not found"**: Ensure all libraries (pandas, plotly, altair) are listed in `requirements.txt`.
* **"File not found"**: Check your folder structure. If `Home.py` is inside a folder, you must specify that path in the deployment settings.

## How to Update Your App

Once deployed, your app is connected to GitHub. To make changes:

1. **Edit the code** on your computer.
2. **Push the changes** to GitHub:

    ```bash
    git add .
    git commit -m "Description of changes"
    git push
    ```

3. **That's it!** Streamlit Cloud will detect the new code and automatically update your live app within minutes.
