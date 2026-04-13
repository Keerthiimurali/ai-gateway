import csv
import time
from models import call_capable_model
from cost import calculate_cost_inr

def run_baseline():
    total_tokens = 0
    total_latency = 0
    total_cost = 0

    with open("test_prompts.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompt = row["prompt"]

            start = time.time()
            response, tokens = call_capable_model(prompt)
            latency = time.time() - start

            # Cost calculation (always capable model)
            cost = calculate_cost_inr("capable", tokens)

            total_tokens += tokens
            total_latency += latency
            total_cost += cost

            print(
                f"Prompt: {prompt} | Tokens: {tokens} | "
                f"Latency: {latency:.2f}s | Cost: ₹{cost:.4f}"
            )

    print("\n BASELINE (Always Capable Model):\n")
    print(f"Total Tokens: {total_tokens}")
    print(f"Total Latency: {total_latency:.2f}s")
    print(f"Total Cost: ₹{total_cost:.4f}")

    # ✅ THIS IS THE MOST IMPORTANT FIX
    return total_tokens, total_latency, total_cost


if __name__ == "__main__":
    run_baseline()