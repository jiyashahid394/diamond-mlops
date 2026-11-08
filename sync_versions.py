"""Write the exact library and Python versions of THIS laptop into
requirements.txt, requirements-dev.txt, the Dockerfile and the pipeline.

Why: a model saved with one scikit-learn version can fail to load under
another. Run it after every change of your Python environment.
"""
import os
import re
import sys
from importlib.metadata import version

SERVE = ["fastapi", "uvicorn", "pydantic", "scikit-learn", "pandas",
         "numpy", "joblib", "prometheus-client", "cloudpickle"]
DEV = ["mlflow", "scipy", "pytest", "httpx", "requests", "dvc", "dvc-s3"]
py = f"{sys.version_info.major}.{sys.version_info.minor}"

with open("requirements.txt", "w") as f:
    f.write("\n".join(f"{p}=={version(p)}" for p in SERVE) + "\n")
with open("requirements-dev.txt", "w") as f:
    f.write("-r requirements.txt\n")
    f.write("\n".join(f"{p}=={version(p)}" for p in DEV) + "\n")

updated = ["requirements.txt", "requirements-dev.txt"]
for path, pattern, new in [
    ("Dockerfile", r"python:[\d.]+-slim", f"python:{py}-slim"),
    (".github/workflows/ml-pipeline.yml",
     r'python-version: "[\d.]+"', f'python-version: "{py}"'),
]:
    if not os.path.exists(path):
        print(f"(skipped {path}: file does not exist yet)")
        continue
    text = open(path).read()
    open(path, "w").write(re.sub(pattern, new, text))
    updated.append(path)

print(f"Python {py}; updated: " + ", ".join(updated))
