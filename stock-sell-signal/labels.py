import pandas as pd
def create_labels(input_csv, output_csv):
    df = pd.read_csv(input_csv)


    # 1. Get the Future close prices( for next 5 days)
    df["future_close_5d"] = df["Close"].shift(-5)  # It looks 5 rows down (into the future) and pulls that price up to the current row.
    # shift(-1) = Jump 1 day into the future.
    # shift(-5) = Jump 5 days into the future.
    # shift(-30) = Jump 30 days into the future.

    # In your data: Look at the row for Jan 05. The "Close" is 111.
    # The code looks 5 days ahead to Jan 10, where the "Close" was 105.
    # It takes that 105 and writes it in a new column on the Jan 05 row.
    # Result: Now, the Jan 05 row knows what happens on Jan 10.

    # Data at the "Close" column in our csv file:
    # Jan 05: Price is 111 (This is "Today")
    # Jan 06: 113
    # Jan 07: 114
    # Jan 08: 115
    # Jan 09: 117
    # Jan 10: Price is 105 (This is "Today + 5 days")
    # When you run df["Close"].shift(-5)
    # Python goes to the Jan 05 row, jumps over the next 4 days, grabs the 105 from Jan 10, 
    # and brings it back to the Jan 05 as below by adding new column
    # Date     Close(Today)   future_close_5d
    # Jan 05   111            105

    # 2: Calculate the "Raw Change"
    # (105 - 111) = -6 i.e Jan 5th 105 and Jan 11th it's 105
    # This shows we lost 6rs over those 5 days.
    raw_change = df["future_close_5d"] - df["Close"]


    # 3: Convert to a "Percentage Return"
    # We divide the 6rs loss by our starting price of 111rs.
    # -6 / 111 = -0.054 (A 5.4% loss)
    # This makes the data "comparable" even if the stock price grows to 1000rs later.
    df["future_return_5d"] = raw_change / df["Close"]

    # 4: The "Sell" Decision (The Label)
    # We ask: Is the return worse than a 1% drop?
    # -0.054 is definitely lower than -0.01.
    # This results in 'True'.
    is_it_a_drop = (df["future_return_5d"] < -0.01)

    # STEP 5: Convert 'True/False' to '1/0'
    # AI models don't like words or Boolean values; they want numbers.
    # .astype(int) turns 'True' into 1 and 'False' into 0.
    # Result: Jan 5th gets a "1" (SELL)
    df["sell"] = is_it_a_drop.astype(int)   # The int argument tells Pandas: "Convert these 
    # logical True/False values into the Integer data type."

    # 4. Drop rows, where label "sell" cannot be computed i.e rows having NaN
    df = df.dropna()  # If any single column in a row is empty, delete the whole row.

    # 5. save labelled data
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    create_labels("stock_features.csv", "stock_labelled.csv")
