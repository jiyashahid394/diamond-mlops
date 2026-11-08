"""Send fake user traffic to the API.

Usage: python send_traffic.py normal   (diamonds like the training data)
       python send_traffic.py drift    (large diamonds, 1.8 to 3.0 carat)
"""
import random
import sys

import pandas as pd
import requests

URL = "http://localhost:8080/predict"
mode = sys.argv[1] if len(sys.argv) > 1 else "normal"
rows = pd.read_csv("diamonds.csv")

for _ in range(60):
    row = rows.sample(1).iloc[0]
    body = {"carat": float(row["carat"]),
            "depth": float(row["depth"]),
            "table": float(row["table"])}
    if mode == "drift":
        body["carat"] = round(random.uniform(1.8, 3.0), 2)  # big stones
    r = requests.post(URL, json=body, timeout=5)
    r.raise_for_status()
print(f"Sent 60 {mode} requests")
