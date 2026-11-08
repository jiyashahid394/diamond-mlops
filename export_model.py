"""Save the registry champion as champion.pkl (the file the API loads)."""
import joblib
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("sqlite:///mlflow.db")
model = mlflow.sklearn.load_model("models:/diamond-price-model@champion")
joblib.dump(model, "champion.pkl")
print("Saved champion.pkl")
