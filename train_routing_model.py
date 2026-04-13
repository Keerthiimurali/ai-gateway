import csv
import joblib
from sklearn.linear_model import LogisticRegression

# -------------------------------
# SAME FEATURE LOGIC AS ROUTING
# -------------------------------
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

# -------------------------------
# FEATURE EXTRACTION (SAME AS ROUTING)
# -------------------------------
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

# -------------------------------
# LOAD DATA
# -------------------------------
def load_data(file="train_prompts.csv"):
    X, y = [], []

    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            features = extract_features(row["prompt"])
            label = 1 if row["label"] == "complex" else 0

            X.append(features)
            y.append(label)

    return X, y

# -------------------------------
# TRAIN MODEL
# -------------------------------
def train_model():
    X, y = load_data()

    model = LogisticRegression()
    model.fit(X, y)

    joblib.dump(model, "routing_model.pkl")
    print("✅ Feature-based routing model trained and saved!")

if __name__ == "__main__":
    train_model()