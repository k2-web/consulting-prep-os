#!/bin/bash
echo "🚀 Starting Publication Process..."

# Add all changes
git add .

# Commit changes
git commit -m "Final deployment readiness fixes"

# Push to GitHub
echo "📦 Uploading to GitHub..."
echo "👉 You may be asked for your GitHub username and password/token."
git push -u origin main

echo "✅ Done! Now go to https://share.streamlit.io to deploy."
