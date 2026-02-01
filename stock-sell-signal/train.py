import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

print("RUNNING TRAIN.PY FROM:", __file__)
def train_model(csv_path):
    df = pd.read_csv(csv_path)



    # select features and label
    X = df[["ma_5", "price_vs_ma5", "daily_returns"]]
    y = df["sell"]
    
    print("TOTAL ROWS:", len(df))

    # Time based split
    split_index = int(len(df) * 0.7)
    print("SPLIT INDEX:", split_index)

    X_train = X.iloc[:split_index]
    y_train = y.iloc[:split_index]

    X_test = X.iloc[split_index:]
    y_test = y.iloc[split_index:]
    print("TRAIN ROWS:", len(X_train))
    print("TEST ROWS:", len(X_test))

    # Train a simple model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate on same data
    preds = model.predict(X_test)

    print(classification_report(y_test, preds))

if __name__ == "__main__":
    train_model("stock_labelled.csv")