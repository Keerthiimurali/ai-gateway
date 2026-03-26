import csv
import time
from routing import routing_model
from models import call_fast_model, call_capable_model

def run_smart_routing():
    total_tokens = 0
    total_latency = 0
    with open("test_prompts.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row["prompt"]

           
            decision, reason, confidence = routing_model(prompt)

            start = time.time()
            if decision == "fast":
                response, tokens = call_fast_model(prompt)
            else:
                response, tokens = call_capable_model(prompt)
            latency = time.time() - start

            total_tokens += tokens
            total_latency += latency

            print(f"Prompt: {prompt} | Routed: {decision} | Reason: {reason} | Confidence: {confidence:.2f} | Tokens: {tokens} | Latency: {latency:.2f}s")

    print("\nSmart Routing:\n")
    print(f"Total Tokens: {total_tokens}")
    print(f"Total Latency: {total_latency:.2f}s")

if __name__ == "__main__":
    run_smart_routing()
