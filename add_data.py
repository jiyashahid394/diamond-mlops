"""Safely append a batch of new diamonds to diamonds.csv.

Usage: python add_data.py data_batches/batch2_new.csv
"""
import sys

import pandas as pd

COLUMNS = ["carat", "depth", "table", "price_usd"]

batch = pd.read_csv(sys.argv[1])
main = pd.read_csv("diamonds.csv")

assert list(batch.columns) == COLUMNS, "columns do not match diamonds.csv"
assert not batch.isnull().any().any(), "batch has empty cells"
assert (batch > 0).all().all(), "all values must be positive"

combined = pd.concat([main, batch], ignore_index=True).drop_duplicates()
combined.to_csv("diamonds.csv", index=False)
print(f"diamonds.csv now has {len(combined)} rows "
      f"({len(combined) - len(main)} added)")
