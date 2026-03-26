import csv
import time
from models import call_capable_model   

def run_baseline():
    total_tokens = 0
    total_latency = 0
    with open("test_prompts.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row["prompt"]
            start = time.time()
            response, tokens = call_capable_model(prompt)
            latency = time.time() - start
            total_tokens += tokens
            total_latency += latency
            print(f"Prompt: {prompt} | Tokens: {tokens} | Latency: {latency:.2f}s")

    print("\nBaseline (Always Capable):\n")
    print(f"Total Tokens: {total_tokens}")
    print(f"Total Latency: {total_latency:.2f}s")

if __name__ == "__main__":
    run_baseline()
