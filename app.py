"""FastAPI service: health, predict and metrics endpoints."""
import csv
import os
import time
from datetime import datetime, timezone

import joblib
import pandas as pd
from fastapi import FastAPI
from prometheus_client import (CONTENT_TYPE_LATEST, Counter, Histogram,
                               generate_latest)
from pydantic import BaseModel, Field
from starlette.responses import Response

FEATURES = ["carat", "depth", "table"]
DIARY = "predictions.csv"

app = FastAPI(title="Diamond Price API")
model = joblib.load("champion.pkl")  # loaded once at startup

PREDICTIONS = Counter("predictions_total", "Number of predictions served")
LATENCY = Histogram("prediction_seconds", "Time to answer one prediction")
CARAT = Histogram("input_carat", "Carat size asked by users",
                  buckets=[0.25, 0.5, 0.75, 1, 1.5, 2, 3, 5])
PRICE = Histogram("predicted_price_usd", "Predicted price in USD",
                  buckets=[500, 1000, 2500, 5000, 10000, 15000, 20000])


class Diamond(BaseModel):
    carat: float = Field(gt=0)
    depth: float = Field(gt=0)
    table: float = Field(gt=0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(diamond: Diamond):
    start = time.time()
    row = pd.DataFrame([[diamond.carat, diamond.depth, diamond.table]],
                       columns=FEATURES)
    price = float(model.predict(row)[0])

    PREDICTIONS.inc()
    CARAT.observe(diamond.carat)
    PRICE.observe(price)
    LATENCY.observe(time.time() - start)

    new_file = not os.path.exists(DIARY)
    with open(DIARY, "a", newline="") as f:  # the prediction diary
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["time"] + FEATURES + ["price_usd"])
        writer.writerow([datetime.now(timezone.utc).isoformat(),
                         diamond.carat, diamond.depth, diamond.table,
                         round(price, 1)])
    return {"price_usd": round(price, 1)}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
