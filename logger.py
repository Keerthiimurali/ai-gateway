import json
from datetime import datetime
import os

LOG_FILE = "gateway_logs.json"



# STEP 1: Append log entry

def append_log(entry: dict):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []

    # Add timestamp automatically
    entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logs.append(entry)

    # Save back to file
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)



# STEP 2: Read logs

def read_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []



# STEP 3: Cache Hit Rate Metric

def compute_cache_hit_rate():
    if not os.path.exists(LOG_FILE):
        print("No logs found.")
        return 0

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    total_requests = len(logs)
    cache_hits = sum(1 for log in logs if log.get("cache_hit") is True)

    if total_requests == 0:
        return 0

    hit_rate = (cache_hits / total_requests) * 100

    print("\nCACHE METRICS:\n")
    print(f"Total Requests: {total_requests}")
    print(f"Cache Hits: {cache_hits}")
    print(f"Cache Hit Rate: {hit_rate:.2f}%")

    return hit_rate