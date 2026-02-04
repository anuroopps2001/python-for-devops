import joblib
import os
import time
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response
from fastapi import HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST


MODEL_PATH = "model_v1.pkl"
app = FastAPI(title="Stock Sell Inference API")  # This is how to define an app based on FastAPI docs

# Load model once at startup
print("Loading model artifact")
model = joblib.load(MODEL_PATH)
print("Model loaded successfully")



REQUEST_COUNT = Counter(                 # "Counter" is A cumulative metric that can only increase
    "prediction_requests_total",         # This is an actual metric
    "Total number of prediction requests"  # This is description of that metric
)

ERROR_COUNT = Counter(
    "predictions_error_total",
    "Total number of prediction errors"
)

PREDICTION_LATENCY = Histogram(           # Used for sampling observations, like request durations, and providing quantiles. 
     "prediction_latency_seconds",
     "Time spent processing prediction requests"
)

SELL_SIGNAL_COUNT = Counter(
    "sell_signal_total",
    "Number of sell signals triggered"
)

SELL_THRESHOLD = float(os.getenv("SELL_THRESHOLD", "0.7"))  # getenv() is used to access an env variable specified
# at first arg


# Defining a class 
class StockFeatures(BaseModel):
    ma_5: float
    price_vs_ma5: float
    daily_returns: float


# /health point API on GET method
@app.get("/health")
def health():
    return {"status": "Ok"}


# API to an add input details
@app.post("/predict")
def predict_sell_probability(features: StockFeatures):  # features is an parameter of type StockFeatures (which is an class)
    # X = np.array([[
    #     features.ma_5,
    #     features.price_vs_ma5,
    #     features.daily_returns
    # ]])

    REQUEST_COUNT.inc()  # inc() increment the count by 1 which is default value

    # # Record the start time using perf_counter()
    start_time = time.perf_counter() 

    try:

        features_data = pd.DataFrame([{
            features.ma_5,
            features.price_vs_ma5,
            features.daily_returns
        }])

        sell_prob = model.predict_proba(features_data)[0][1]  # calling model to predict the sell probability

        sell_signal = bool(sell_prob >= SELL_THRESHOLD)
        if sell_signal:
            SELL_SIGNAL_COUNT.inc()

        # # Record the end time
        end_time = time.perf_counter()

        # Calculate the duration (latency) in seconds
        latency = end_time - start_time

        # call the metric with latency calculated
        PREDICTION_LATENCY.observe(latency)


        return {
              "raw_probability": round(float(sell_prob), 4),
              "sell_signal": sell_signal,
              "threshold": SELL_THRESHOLD
        }
    except Exception as e:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=500, detail=str(e))


# Exposing metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)