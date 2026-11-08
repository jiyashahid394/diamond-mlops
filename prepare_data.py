"""Download the public Diamonds dataset and prepare the three data files.

Source (free, no login): seaborn-data on GitHub, 53,940 real diamonds.
Run once:  python prepare_data.py

Creates
  diamonds.csv                        300 small diamonds (carat 1.2 or less)
  data_batches/batch2_new.csv          30 more small diamonds (normal new data)
  data_batches/batch3_large.csv        15 large diamonds (carat 1.8 to 3.0)
"""
import os

import pandas as pd

URL = ("https://raw.githubusercontent.com/mwaskom/seaborn-data/"
       "master/diamonds.csv")
COLUMNS = ["carat", "depth", "table", "price_usd"]

raw = pd.read_csv(URL).rename(columns={"price": "price_usd"})
raw = raw[COLUMNS].dropna()
print(f"Downloaded {len(raw)} diamonds")

small = raw[raw["carat"] <= 1.2]
base = small.sample(300, random_state=42)
batch2 = small.drop(base.index).sample(30, random_state=1)
large = raw[(raw["carat"] >= 1.8) & (raw["carat"] <= 3.0)]
batch3 = large.sample(15, random_state=3)

os.makedirs("data_batches", exist_ok=True)
base.to_csv("diamonds.csv", index=False)
batch2.to_csv("data_batches/batch2_new.csv", index=False)
batch3.to_csv("data_batches/batch3_large.csv", index=False)
print("Created diamonds.csv (300 rows), batch2_new.csv (30), batch3_large.csv (15)")
