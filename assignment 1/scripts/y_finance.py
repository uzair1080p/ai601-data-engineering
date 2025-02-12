import yfinance as yf
import csv

def fetch_financial_data(tickers, start_date="2022-01-01", end_date="2024-01-01"):
    data = {}
    
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)["Close"]
        
        for date, price in hist.items():
            date_str = date.strftime("%Y-%m-%d")
            if date_str not in data:
                data[date_str] = {}
            data[date_str][ticker] = price

    return data

def save_to_csv(data, filename, tickers):

    headers = ["Date"] + tickers

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for date in sorted(data.keys()):
            row = [date] + [data[date].get(ticker, "N/A") for ticker in tickers]
            writer.writerow(row)


tickers = ["TSLA", "NIO", "RIVN"]


finance_data = fetch_financial_data(tickers)


save_to_csv(finance_data, "datasets/raw/yfinance.csv", tickers)

print("Yahoo Finance data saved successfully.")
