import json

def generate_data_js():
    # Load quantitative data
    try:
        with open('market_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: market_data.json not found. Run fetch_market_data.py first.")
        return

    # Qualitative Data (Synthesized from research)
    # Added Financial Analysis and Peer Context
    qualitative_insights = {
        "TSLA": {
            "moat": {
                "score": 85,
                "details": [
                    "**FSD Data Advantage**: Over 3 billion miles of real-world driving data.",
                    "**Supercharger Network**: NACS adoption creates infrastructure dominance.",
                    "**Vertical Integration**: In-house battery production and Gigacasting."
                ]
            },
            "management": {
                "score": 80,
                "details": "Elon Musk's visionary leadership is balanced by governance risks due to his split focus."
            },
            "sentiment": {
                "score": 60,
                "label": "Mixed / Volatile",
                "details": "Short-term bearishness due to EV demand slowing; Long-term bullish on Robotaxi."
            },
            "financialAnalysis": "Tesla's revenue growth has moderated to **single digits** in recent quarters as the EV market matures. Margins have compressed due to aggressive price cuts aimed at defending market share. However, **Net Income** remains robust compared to legacy peers, driven by regulatory credits and energy storage profitability. The key metric to watch is **Auto Gross Margin ex-credits**, which needs to stabilize above 17%."
        },
        "NVDA": {
            "moat": {
                "score": 98,
                "details": [
                    "**CUDA Ecosystem**: Deep software moat with 4M+ developers.",
                    "**Hardware Dominance**: 90%+ share in AI GPUs (Blackwell).",
                    "**Innovation Pace**: Annual release cycles keep competitors behind."
                ]
            },
            "management": {
                "score": 95,
                "details": "Jensen Huang is executing flawlessly on the AI infrastructure roadmap."
            },
            "sentiment": {
                "score": 90,
                "label": "Extremely Bullish",
                "details": "Riding the massive AI wave with record revenues and margins."
            },
            "financialAnalysis": "Nvidia is exhibiting **hyper-growth**, with revenue doubling year-over-year. **Gross Margins** are exceptional at ~75%, reflecting immense pricing power and shortage of supply. Operating leverage is kicking in, expanding Net Income margins significantly. The primary financial risk is a potential 'air pocket' in demand if hyperscalers pause capex, but current visibility remains strong."
        },
        "AAPL": {
            "moat": {
                "score": 95,
                "details": [
                    "**Ecosystem Lock-in**: iOS 'Walled Garden' creates high retention.",
                    "**Services Growth**: High-margin recurring revenue (App Store, iCloud).",
                    "**Brand Power**: Unmatched pricing power in consumer electronics."
                ]
            },
            "management": {
                "score": 90,
                "details": "Tim Cook continues to demonstrate operational excellence and capital return discipline."
            },
            "sentiment": {
                "score": 75,
                "label": "Cautiously Optimistic",
                "details": "Concerns over iPhone China sales vs 'Apple Intelligence' upgrade cycle."
            },
            "financialAnalysis": "Apple's top-line growth is **steady but slow**, characteristic of a mature stalwart. The growth engine has shifted to **Services**, which now accounts for ~25% of revenue with double the margins of hardware. **Free Cash Flow** generation is massive, fueling aggressive share buybacks that support EPS growth even when revenue is flat."
        },
        "NKE": {
            "moat": {
                "score": 70,
                "details": [
                    "**Brand Heritage**: The 'Swoosh' remains one of the most recognizable logos globally.",
                    "**Athlete Endorsements**: Dominance in basketball and running sponsorships.",
                    "**DTC Scale**: Strong direct-to-consumer digital channels."
                ]
            },
            "management": {
                "score": 65,
                "details": "Recent leadership changes reflect a need to pivot back to product innovation after a period of stagnation."
            },
            "sentiment": {
                "score": 40,
                "label": "Bearish / Turnaround",
                "details": "Struggling with inventory issues, China slowdown, and rising competition from Hoka/On."
            },
            "financialAnalysis": "Nike is currently in a **turnaround phase**. Revenue growth has turned negative/flat due to weakness in North America and Greater China. **Gross Margins** are under pressure from promotional activity to clear inventory. The company is cutting costs to protect profitability, but a return to sustainable growth depends on the success of new product innovation cycles."
        }
    }

    # Manual Price Overrides (Fallback)
    price_overrides = {
        "TSLA": 430.00,
        "NVDA": 138.00,
        "AAPL": 235.00,
        "NKE": 78.00
    }

    # Merge data
    from fetch_llm_data import fetch_llm_data

    for ticker, insights in qualitative_insights.items():
        if ticker in data:
            data[ticker]['qualitative'] = insights
            
            # 1. Try fetching Live Data from LLM
            print(f"Attempting to fetch live data for {ticker}...")
            llm_data = fetch_llm_data(ticker)
            
            if llm_data and 'price' in llm_data:
                print(f"Success! Updated {ticker} with live data: ${llm_data['price']}")
                data[ticker]['technicals']['currentPrice'] = llm_data['price']
                if 'marketCap' in llm_data:
                    data[ticker]['ratios']['marketCap'] = llm_data['marketCap']
                if 'analysis' in llm_data:
                    data[ticker]['qualitative']['financialAnalysis'] = llm_data['analysis']
                
                # Update last price history point
                if data[ticker]['priceHistory']:
                    data[ticker]['priceHistory'][-1]['close'] = llm_data['price']
            
            # 2. Fallback to Manual Overrides if LLM failed and override exists
            elif ticker in price_overrides:
                print(f"LLM fetch failed or skipped. Using manual override for {ticker}.")
                data[ticker]['technicals']['currentPrice'] = price_overrides[ticker]
                if data[ticker]['priceHistory']:
                    data[ticker]['priceHistory'][-1]['close'] = price_overrides[ticker]
            
            # Add Industry Averages (Mock data for now, ideally fetched)
            data[ticker]['industry'] = {
                "pe": 25.0 if ticker != 'NVDA' else 40.0,
                "margins": 0.15 if ticker != 'NVDA' else 0.50
            }

    # Write to data.js
    js_content = f"const marketData = {json.dumps(data, indent=4)};"
    
    with open('slide_deck/data.js', 'w') as f:
        f.write(js_content)
    
    print("Successfully generated slide_deck/data.js")

if __name__ == "__main__":
    generate_data_js()
