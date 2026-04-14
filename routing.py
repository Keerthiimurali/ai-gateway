import joblib
import numpy as np


# LOAD TRAINED MODEL

model = joblib.load("routing_model.pkl")


# FEATURE DEFINITIONS

COMPLEX_KEYWORDS = [
    "explain", "analyze", "compare", "why", "how",
    "implement", "code", "algorithm", "debug",
    "design", "architecture",
    "neural", "network", "machine learning", "ai",
    "summarize", "function", "write", "steps",
    "process", "difference"
]

CODE_KEYWORDS = [
    "code", "function", "program", "debug",
    "algorithm", "implement", "script"
]

SIMPLE_PATTERNS = [
    "how are you", "hello", "hi"
]

# Tuned threshold
THRESHOLD = 0.65

# FEATURE EXTRACTION FUNCTION

def extract_features(prompt: str):
    prompt_lower = prompt.lower()

    word_count = len(prompt.split())
    keyword_flag = int(any(word in prompt_lower for word in COMPLEX_KEYWORDS))
    code_flag = int(
        any(word in prompt_lower for word in CODE_KEYWORDS) or
        any(symbol in prompt for symbol in ["def", "class", "{", "}", ";"])
    )
    simple_flag = int(any(pattern in prompt_lower for pattern in SIMPLE_PATTERNS))
    question_flag = int("?" in prompt)

    return [
        word_count,
        keyword_flag,
        code_flag,
        simple_flag,
        question_flag
    ]


# MAIN ROUTING FUNCTION

def routing_model(prompt: str):
    prompt_lower = prompt.lower()

    # STEP 1: Extract features
    features = extract_features(prompt)

    # STEP 2: ML prediction
    prob = model.predict_proba([features])[0][1]  # P(complex)

    # STEP 3: Feature unpacking
    word_count, keyword_flag, code_flag, simple_flag, question_flag = features

    # STEP 4: Controlled tuning (light adjustments only)
    if word_count > 12:
        prob += 0.05

    if keyword_flag:
        prob += 0.05   

    if code_flag:
        prob += 0.15   

    if simple_flag:
        prob -= 0.15   

    
    prob = max(0.0, min(prob, 1.0))

   
    signals = []

    if word_count > 12:
        signals.append("long prompt")

    if keyword_flag:
        signals.append("complex keywords")

    if code_flag:
        signals.append("code/technical task")

    if question_flag:
        signals.append("question")

    if simple_flag:
        signals.append("simple pattern")

    signal_text = ", ".join(signals) if signals else "no strong signals"

  
    if code_flag:
        decision = "capable"
        reason = f"Override → Capable Model (code detected, score={prob:.2f})"

    elif keyword_flag and prob >= 0.7:
        decision = "capable"
        reason = f"Override → Capable Model (high-confidence keywords, score={prob:.2f})"

    elif prob > THRESHOLD:
        decision = "capable"
        reason = f"High complexity ({prob:.2f}) → Capable Model ({signal_text})"

    else:
        decision = "fast"
        reason = f"Low complexity ({prob:.2f}) → Fast Model ({signal_text})"

   
    confidence = prob if decision == "capable" else 1 - prob

    return decision, reason, confidence, signals