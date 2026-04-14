import csv
import time
from routing import routing_model
from models import call_fast_model, call_capable_model
from cost import calculate_cost_inr


def run_smart_routing():
    total_tokens = 0
    total_latency = 0
    total_cost = 0

    with open("test_prompts.csv", "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            prompt = row["prompt"]

            
            # Step 1: Routing decision
            
            decision, reason, confidence, signals = routing_model(prompt)

           
            # Step 2: Model execution
           
            start = time.time()

            if decision == "fast":
                response, tokens = call_fast_model(prompt)
            else:
                response, tokens = call_capable_model(prompt)

            latency = time.time() - start

            
            if tokens == 0:
                tokens = len(prompt.split())

           
            # Step 3: Cost calculation
            
            cost = calculate_cost_inr(decision, tokens)

            total_tokens += tokens
            total_latency += latency
            total_cost += cost

            print(
                f"Prompt: {prompt} | Routed: {decision} | "
                f"Reason: {reason} | Confidence: {confidence:.2f} | "
                f"Tokens: {tokens} | Latency: {latency:.2f}s | Cost: ₹{cost:.4f}"
            )

    print("\n SMART ROUTING RESULTS:\n")
    print(f"Total Tokens: {total_tokens}")
    print(f"Total Latency: {total_latency:.2f}s")
    print(f"Total Cost: ₹{total_cost:.4f}")

    return total_tokens, total_latency, total_cost



#  Compare with Baseline

if __name__ == "__main__":
    from baseline import run_baseline

    print("\n Running BASELINE...\n")
    base_tokens, base_latency, base_cost = run_baseline()

    print("\n Running SMART ROUTING...\n")
    smart_tokens, smart_latency, smart_cost = run_smart_routing()

    

    # Token savings
    if base_tokens == 0:
        token_savings = 0
    else:
        token_savings = ((base_tokens - smart_tokens) / base_tokens) * 100

    # Latency savings
    if base_latency == 0:
        latency_savings = 0
    else:
        latency_savings = ((base_latency - smart_latency) / base_latency) * 100

    # Cost savings
    if base_cost == 0:
        cost_savings = 0
    else:
        cost_savings = ((base_cost - smart_cost) / base_cost) * 100

    print("\n FINAL COMPARISON:\n")
    print(f"Token Savings: {token_savings:.2f}%")
    print(f"Latency Savings: {latency_savings:.2f}%")
    print(f"Cost Savings: {cost_savings:.2f}%")