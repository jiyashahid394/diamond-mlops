"""Compare the last 50 live requests with the training data (KS test)."""
import sys

import pandas as pd
from scipy.stats import ks_2samp

FEATURES = ["carat", "depth", "table"]
THRESHOLD = 0.01

train = pd.read_csv("diamonds.csv")
live = pd.read_csv("predictions.csv").tail(50)
print(f"Comparing {len(live)} live requests with {len(train)} training rows")

drift = False
for col in FEATURES:
    stat, p = ks_2samp(train[col], live[col])
    flag = "DRIFT" if p < THRESHOLD else "ok"
    drift |= p < THRESHOLD
    print(f"{col:12s} KS={stat:.2f}  p-value={p:.4f}  {flag}")

print("RESULT: DRIFT DETECTED" if drift else "RESULT: no drift")
sys.exit(1 if drift else 0)
