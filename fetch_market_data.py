import yfinance as yf
import json
import time

# Main Tickers and their Peers
TICKERS = {
    'TSLA': ['TM', 'F', 'BYDDF'],
    'NVDA': ['AMD', 'INTC'],
    'AAPL': ['MSFT', 'GOOGL'],
    'NKE': ['ADS.DE', 'LULU'] # Added Nike as per user mention
}

def fetch_live_data():
    print("Fetching live market data...")
    live_data = {}
    
    for ticker in TICKERS:
        try:
            print(f"Fetching {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract relevant data
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            market_cap = info.get('marketCap', 0)
            trailing_pe = info.get('trailingPE', 0)
            forward_pe = info.get('forwardPE', 0)
            beta = info.get('beta', 0)
            
            # Financials (Mocking some if missing or complex to parse consistently)
            # In a real robust app, we'd parse stock.financials deeply.
            # For this demo, we'll focus on the Price and key Ratios being real.
            
            # Use trailingPE if available, otherwise forwardPE, or 0
            pe_ratio = trailing_pe if trailing_pe else forward_pe

            live_data[ticker] = {
                "price": current_price,
                "ratios": {
                    "marketCap": market_cap,
                    "pe": pe_ratio
                }
            }
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            # Fallback to 0 or skip
            live_data[ticker] = {"price": 0, "ratios": {}}

    return live_data

def generate_js_file(data):
    js_content = f"const LIVE_MARKET_DATA = {json.dumps(data, indent=4)};"
    
    output_path = 'slide_deck/live_data.js'
    with open(output_path, 'w') as f:
        f.write(js_content)
    
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    data = fetch_live_data()
    generate_js_file(data)
