# Deployment Guide: Consulting Prep OS

This guide will help you deploy your application to **Streamlit Cloud** so you can share it with friends.

## Prerequisites

1. A **GitHub Account** (free).
2. A **Streamlit Cloud Account** (free, sign up with GitHub).

## Step 1: Prepare Your Code

Ensure your project folder (`consulting-prep`) has the following structure:

```
consulting-prep/
├── Home.py                  # Main Dashboard
├── pages/                   # All other pages
│   ├── 1_Case_Library.py
│   ├── 2_Active_Case.py
│   ├── 3_My_Performance.py
│   └── 4_Learning_Resources.py
├── utils.py                 # Shared CSS/Config
├── backend.py               # Session Logic
├── content/                 # Markdown files
├── requirements.txt         # Dependencies
└── .streamlit/
    └── config.toml          # Theme settings
```

## Step 2: Push to GitHub

1. Create a new **Public Repository** on GitHub (e.g., `consulting-prep-app`).
2. Upload all files from the `consulting-prep` folder to this repository.
    * *Tip: You can drag and drop files directly into the GitHub web interface if you don't use Git command line.*

## Step 3: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Click **"New app"**.
3. Select your GitHub repository (`consulting-prep-app`).
4. **Main file path**: Enter `Home.py`.
5. Click **"Deploy!"**.

## Step 4: Share

Once deployed, Streamlit will give you a URL (e.g., `https://consulting-prep-app.streamlit.app`).
Send this link to your friend. They can access it from any device (laptop, tablet, phone).

## Troubleshooting

* **"Module not found"**: Ensure `requirements.txt` includes `streamlit`, `pandas`, and `altair`.
* **"File not found"**: Ensure your `content` folder is uploaded and paths in code use `os.path.abspath`.
