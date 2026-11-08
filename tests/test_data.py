import pandas as pd

COLUMNS = ["carat", "depth", "table", "price_usd"]
df = pd.read_csv("diamonds.csv")


def test_columns():
    assert list(df.columns) == COLUMNS


def test_no_empty_cells():
    assert not df.isnull().any().any()


def test_all_values_positive():
    assert (df > 0).all().all()


def test_enough_rows():
    assert len(df) >= 40
