# cost.py

# Pricing in USD per 1000 tokens
COST_PER_1K_TOKENS = {
    "fast": 0.0002,
    "capable": 0.002
}

USD_TO_INR = 83  # conversion rate


def calculate_cost_inr(model_type, tokens):
    # cost per token in USD
    cost_per_token_usd = COST_PER_1K_TOKENS[model_type] / 1000

    # total cost in USD
    total_cost_usd = tokens * cost_per_token_usd

    # convert to INR
    total_cost_inr = total_cost_usd * USD_TO_INR

    return total_cost_inr