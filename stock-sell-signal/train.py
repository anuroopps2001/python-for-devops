import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


## Train on the past 70% data, test on the future 30% data
print("RUNNING TRAIN.PY FROM:", __file__)
def train_model(csv_path):
    df = pd.read_csv(csv_path)  # reading an data frame
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=True).reset_index(drop=True)

    dates = df["Date"]   # # keep dates separately

    # select features and label
    # This is like, creating new csv with below columns only on each row
    X = df[["ma_5", "price_vs_ma5", "daily_returns"]]  # X (Features): These are the variables the AI is allowed to 
    # look at to make a decision. In our case, it's the Past data (averages and returns).


    # This is also, like creating an new csv file adding keeping all the rows with only "sell" column in it
    y = df["sell"]   # y (Label): This is the Target. It’s the "Answer Key" we want the AI to 
    # learn to predict (0 or 1).
    
    print("TOTAL ROWS:", len(df))


    # Time based split
    split_index = int(len(df) * 0.7)  # We take the total number of rows and find the 70% mark.
    print("SPLIT INDEX:", split_index)  # split_index is 14 (70% of 20).


    # iloc: This is a Pandas command that stands for "Integer Location."
    X_training = X.iloc[:split_index]  # Give me every column in X, but only for the first 14 rows.
    y_training = y.iloc[:split_index]  # First 70% of Answers from 0 to 6
    # Train 70% of data


    # Test remaning 30% based on training done earlier
    X_testing = X.iloc[split_index:]   # Remaining 30% of Questions from 7 to 10
    y_testing = y.iloc[split_index:]   # Remaining 30% of Answers  from 7 10

    print("This model will be trained on:", len(X_training), "rows")
    print("and will be tested on remaining:", len(X_testing), "rows")

    dates_test = dates.iloc[split_index:]
     
    # Train a simple model
    model = LogisticRegression()
    model.fit(X_training, y_training)  # Training against the table in X_training with table in y_training
    
    joblib.dump(model, "model_v1.pkl") # storing trained model as an artifact, which we for containarizing
    print("Model saved as model_v1.pkl")

    loaded_module = joblib.load("model_v1.pkl")  # loading back the stored artifact to use it as trained model
    print("\nModel loaded back succesfully")
    # Evaluate on same data
#   predictions = model.predict(X_testing)  # Now testing the model by providing the data and asking model to predict based 
    # scenarios it was trained previously by providing both X_train and y_train data.
    # However, now we are asking model to predict the answers of y_testing based on previous training
    
    sell_probability = loaded_module.predict_proba(X_testing)[:, 1]
    # enumerate() function
    # Ex:- numbers = [10, 20, 30]
    # for n in numbers:
    #    print(n)
    # Output:
    # 10
    # 20
    # 30

    # With enumerate()
    # for i, n in enumerate(numbers):
    #     print(i, n)
    # output:
    # 0 10
    # 1 20
    # 2 30


    # i → index (row number)
    # n → value at that index

    print("\nSELL probabilities for test rows:")
    for i, p in enumerate(sell_probability):  # i is index and p is value at that index
        print(f"Row {i}: SELL probability = {p:.3f}")   # Print p with 3 digits after the decimal

    # The classification_report is like a teacher with two lists. In one hand, 
    # they have the Actual Answer Key (y_testing), and in the other, they have the Student's Answers (predictions).
    
    # Testing model predictions with actual data
    # Think of it like this:
    # AI says: "I predict Row 15 is a 1 (Sell)."
    # You look at y_test: "Row 15 was actually a 1. Good job, AI!"
    # AI says: "I predict Row 16 is a 0 (Hold)."
    # You look at y_test: "Row 16 was actually a 1. Wrong! You missed a drop."


    print("\nSELL Probabilities for test rows with Date of each Stock")
    for date, prob in zip(dates, sell_probability):
        print(f"Date {date}: SELL probability = {prob:.3f}")
if __name__ == "__main__":
    train_model("stock_labelled.csv")