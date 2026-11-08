"""Give the alias 'champion' to the registered version with the lowest MAE."""
import mlflow
from mlflow import MlflowClient

mlflow.set_tracking_uri("sqlite:///mlflow.db")
client = MlflowClient()
NAME = "diamond-price-model"

best_version, best_mae = None, float("inf")
for mv in client.search_model_versions(f"name='{NAME}'"):
    mae = client.get_run(mv.run_id).data.metrics["mae"]
    print(f"version {mv.version}: MAE {mae:.3f}")
    if mae < best_mae:
        best_version, best_mae = mv.version, mae

client.set_registered_model_alias(NAME, "champion", best_version)
print(f"champion is now version {best_version} (MAE {best_mae:.3f})")
