import pandas as pd
import numpy as np


# create an Data Frame
data = {'price': [100, 102, 105, np.nan, 108, 110]}

df = pd.DataFrame(data)

# Calculate the percentage change

df["Price_change_fraction"] = df["price"].pct_change() # (today - yesterday) / yesterday

df["Price_change_percentage"] = df["Price_change_fraction"] * 100

print(df)