import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def fetch_from_perplexity(ticker):
    print(f"Fetching {ticker} data from Perplexity...")
    
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": "You are a financial data API. Return ONLY valid JSON. No markdown formatting."
            },
            {
                "role": "user",
                "content": f"Get the current real-time stock price, market cap, and a brief 2-sentence financial analysis for {ticker}. Return JSON in this format: {{ 'price': <number>, 'marketCap': <number>, 'analysis': '<string>' }}."
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Perplexity Error ({response.status_code}): {response.text}")
        response.raise_for_status()
        result = response.json()
        content = result['choices'][0]['message']['content']
        # Clean markdown if present
        content = content.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except Exception as e:
        print(f"Perplexity Exception: {e}")
        return None

def fetch_llm_data(ticker):
    if PERPLEXITY_API_KEY:
        return fetch_from_perplexity(ticker)
    return None

if __name__ == "__main__":
    # Test
    print(fetch_llm_data("TSLA"))
