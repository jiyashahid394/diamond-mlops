"""Ask the running API.

Usage: python ask_api.py health
       python ask_api.py 0.7 61.5 57          (carat depth table, port 8000)
       python ask_api.py 2.04 61.8 60 8080    (optional port at the end)
"""
import sys

import requests

args = sys.argv[1:]


def number(v):
    try:
        return float(v)
    except ValueError:
        return v  # wrong input on purpose, the API must answer 422


if args[0] == "health":
    base = f"http://localhost:{args[1] if len(args) > 1 else 8000}"
    r = requests.get(f"{base}/health")
else:
    base = f"http://localhost:{args[3] if len(args) > 3 else 8000}"
    body = dict(zip(["carat", "depth", "table"], map(number, args[:3])))
    r = requests.post(f"{base}/predict", json=body)
print(r.status_code, r.json() if r.ok else "input rejected by validation")
