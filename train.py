"""Train one model, log it to MLflow and register it.

Usage: python train.py [forest|linear|tree]   (default: forest)
"""
import json
import sys

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

FEATURES = ["carat", "depth", "table"]
LABEL = "price_usd"
MODELS = {
    "linear": LinearRegression(),
    "tree": DecisionTreeRegressor(random_state=42),
    "forest": RandomForestRegressor(n_estimators=100, random_state=42),
}

kind = sys.argv[1] if len(sys.argv) > 1 else "forest"
df = pd.read_csv("diamonds.csv")
X_train, X_test, y_train, y_test = train_test_split(
    df[FEATURES], df[LABEL], test_size=0.2, random_state=42)

model = MODELS[kind]
model.fit(X_train, y_train)
mae = mean_absolute_error(y_test, model.predict(X_test))

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("diamond-price")
with mlflow.start_run(run_name=kind):
    mlflow.log_param("model_type", kind)
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("rows_in_dataset", len(df))
    mlflow.log_metric("mae", mae)
    mlflow.sklearn.log_model(model, name="model",
                             serialization_format="cloudpickle",
                             registered_model_name="diamond-price-model")

# files used by the tests and by the CI/CD pipeline
joblib.dump(model, "model_latest.pkl")
with open("metrics.json", "w") as f:
    json.dump({"model_type": kind, "mae": round(float(mae), 3),
               "rows": len(df)}, f, indent=2)
print(f"{kind}: MAE = {mae:.2f} USD on {len(df)} diamonds")
