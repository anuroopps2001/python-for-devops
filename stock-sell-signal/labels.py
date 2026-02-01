import pandas as pd
def create_labels(input_csv, output_csv):
    df = pd.read_csv(input_csv)


    # 1. Get the Future close prices( for next 5 days)
    df["future_close_5d"] = df["Close"].shift(-5)


    # 2. Calculate the future return 
    df["future_return_5d"] = (
        df["future_close_5d"] - df["Close"] 
    ) / df["Close"]

    # 3. Create a sell label
    # sell = 1 if price drops more than 3%
    df["sell"] = (df["future_return_5d"] < -0.01).astype(int)


    # 4. Drop rows, where label "sell" cannot be computed
    df = df.dropna()

    # 5. save labelled data
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    create_labels("stock_features.csv", "stock_labelled.csv")
