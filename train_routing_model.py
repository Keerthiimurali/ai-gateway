import csv
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

def load_data(file="test_prompts.csv"):
    prompts, labels = [], []
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prompts.append(row["prompt"])
            labels.append(1 if row["label"] == "complex" else 0)  # 1=complex, 0=simple
    return prompts, labels

def train_model():
    prompts, labels = load_data()

    # Pipeline: vectorize text + logistic regression
    model = Pipeline([
        ("vectorizer", CountVectorizer(max_features=500, ngram_range=(1,2))),
        ("classifier", LogisticRegression())
    ])

    model.fit(prompts, labels)
    joblib.dump(model, "routing_model.pkl")
    print("Routing model trained and saved as routing_model.pkl")

if __name__ == "__main__":
    train_model()
