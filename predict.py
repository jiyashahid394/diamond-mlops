"""Predict one diamond price with the exported champion model."""
import sys

import joblib
import pandas as pd

FEATURES = ["carat", "depth", "table"]

# usage: python predict.py 0.7 61.5 57   (carat, depth %, table %)
carat, depth, table = (float(v) for v in sys.argv[1:4])
model = joblib.load("champion.pkl")
row = pd.DataFrame([[carat, depth, table]], columns=FEATURES)
print(f"Predicted price: {model.predict(row)[0]:.0f} USD")
