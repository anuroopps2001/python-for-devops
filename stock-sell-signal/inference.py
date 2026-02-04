import joblib

import numpy as np
import pandas as pd
MODEL_PATH = "model_v1.pkl"

def load_module():
    print("Loading model artifact")
    try:
        with open(MODEL_PATH, '+rb') as model_artifact_file:
            model = joblib.load(model_artifact_file)
        print("Model loaded successfully")
        return model
    
    except FileNotFoundError:
        print(f"Error: The file {model_artifact_file} was not found")

    except Exception as e:
        print(f"An Error occured {e}")

def predict_sell_probability(model, ma_5: float, price_vs_ma5: float, daily_returns: float):
    features = pd.DataFrame([{
        "ma_5": ma_5,
        "price_vs_ma5": price_vs_ma5,
        "daily_returns": daily_returns
    }])

    sell_probability = model.predict_proba(features)[0][1]
    return sell_probability


if __name__ == "__main__":
    model = load_module()

    ma_5 = 117.4
    price_vs_ma5 = 1.039
    daily_returns = 0.022

    probability = predict_sell_probability(
        model,
        ma_5,
        price_vs_ma5,
        daily_returns
    )

    print(f"SELL Probability: {probability:.3f}")