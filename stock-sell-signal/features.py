# 📌 Problem Statement

# Build a machine-learning–based system that analyzes historical stock price data to estimate short-term downside risk and generate a SELL or HOLD signal.

# The system must:

# 1. Use only historical data (no future leakage)

# 2. Generate interpretable features from price data

# 3. Predict whether the stock price is likely to fall more than 3% in the next 5 trading days

# 4. Produce a clear, logged decision (SELL / HOLD)

# 5. Be reproducible and suitable for production deployment

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def create_features(input_csv, output_csv):
    logging.info(f"Reading input file: {input_csv}")

    # Use the pd.read_csv() function to read an CSV file, passing the file path as an argument.
    df = pd.read_csv(input_csv)

    logging.info(f"Loaded {len(df)} rows")

    # 1. 5-day moving average i,e Rolling Mean :- take the price of the last 5 days, add them up, and divide by 5.
    df["ma_5"] = df["Close"].rolling(5).mean()  # where Close is an column in stocks.csv and it will create 
    # ma_5 column in new output file i,e in stocks_features.csv
    
    # A 5-day moving average means:

    # “Average of today + previous 4 days”


    # 2. Price vs moving average :- {Current Price} / {5-Day Average}
    df["price_vs_ma5"] = df["Close"] / df["ma_5"] # It will take Close and ma_5 columns from stock_featues.csv
    # and calculate the value and create an column called price_vs_ma5 in stock_features.csv



    # 3. Daily returns :- ({Today's Price} - {Yesterday's Price}) / {Yesterday's Price}
    ## df["daily_returns"] = df["Close"].pct_change()  # used to calculate the percentage (fractional) change 
    # between the current and a prior element in a Series or DataFrame. 


    # df["daily_returns"] = (today_close - yesterday_close) / yesterday_close
    # df['Close'].shift(1) gets "Yesterday's Price"
    df["daily_returns"] = (df["Close"] - df["Close"].shift(1)) / df["Close"].shift(1)
    # Now, there will be new column called "daily_returns" created inside stock_features.csv
    


    logging.info(f"Creating 5-day moving average at {output_csv} files")
    df.to_csv(output_csv, index=False)   # to_csv() function is used to write data held within a DataFrame  
    # object to a file in the comma-separated values (CSV) format

if __name__ == "__main__":
    create_features("stocks.csv", "stock_features.csv")

# This Script does below things
# 1. Reads the existing CSV (stocks.csv)

# 2. Loads it into memory as a pandas DataFrame (df)

# 3. Uses existing columns (like Close)

# 4. Performs calculations on those columns

# 5. Creates new columns (ma_5, price_vs_ma5, daily_return)

# 6. Writes everything (old + new columns) into a new CSV file