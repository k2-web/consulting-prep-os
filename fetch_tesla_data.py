import yfinance as yf
import pandas as pd

def fetch_tesla_data():
    print("Fetching data for TSLA...")
    ticker = yf.Ticker("TSLA")
    
    # Get financials (income statement)
    # yfinance returns a DataFrame with dates as columns and metrics as rows
    financials = ticker.financials
    
    if financials.empty:
        print("Error: No financial data found.")
        return

    # Transpose so dates are rows
    financials = financials.T
    
    # Ensure index is datetime
    financials.index = pd.to_datetime(financials.index)
    
    # Sort by date descending
    financials = financials.sort_index(ascending=False)
    
    # We want the last 4 years. 
    # Note: yfinance usually provides annual data by default in 'financials' property for the last 4 years.
    
    target_cols = ['Total Revenue', 'Net Income']
    
    # Check if columns exist
    missing_cols = [col for col in target_cols if col not in financials.columns]
    if missing_cols:
        print(f"Error: Missing columns: {missing_cols}")
        print("Available columns:", financials.columns.tolist())
        return

    data = financials[target_cols].head(4)
    
    # Format for cleaner CSV if needed, but raw numbers are usually better for analysis.
    # We will save the raw numbers.
    
    output_file = "tesla_financials.csv"
    data.to_csv(output_file)
    print(f"Successfully saved {output_file}")
    print(data)

if __name__ == "__main__":
    fetch_tesla_data()
