import joblib

model = joblib.load("routing_model.pkl")

COMPLEX_KEYWORDS = [
    "explain", "analyze", "compare", "why", "how",
    "implement", "code", "algorithm", "debug",
    "design", "architecture",
    "neural", "network", "machine learning", "ai",
    "summarize", "function", "write", "steps",
    "process", "difference"
]

def routing_model(prompt: str):

    prompt_lower = prompt.lower()
    word_count = len(prompt.split())

    # STEP 0: SHORT →  FAST
    if word_count <= 4:
        return "fast", "Very short prompt → Fast model", 0.95

    # STEP 1: RULES 
    if any(word in prompt_lower for word in ["debug", "algorithm", "code"]):
        return "capable", "Code-critical task → Capable model", 0.95
    
    # STEP 2: ML probability
    prob = model.predict_proba([prompt])[0][1]

    # STEP 3: Features 
    keyword_flag = any(word in prompt_lower for word in COMPLEX_KEYWORDS)
    code_flag = any(symbol in prompt for symbol in ["def", "class", "{", "}", ";"])

    if word_count > 10:
        prob += 0.05
    if keyword_flag:
        prob += 0.05
    if "?" in prompt:
        prob += 0.01
    if code_flag:
        prob += 0.15

    prob = min(prob, 1.0)

    # STEP 4:THRESHOLD
    decision = "capable" if prob > 0.8 else "fast"

    # STEP 5: Reason
    if decision == "fast":
        reason = f"Low complexity ({prob:.2f}) → Fast model"
    else:
        reason = f"High complexity ({prob:.2f}) → Capable model"

    confidence = prob if decision == "capable" else 1 - prob

    return decision, reason, confidence