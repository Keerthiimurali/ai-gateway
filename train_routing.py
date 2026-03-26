import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

X = [
    # Simple prompts
    "What is 2+2?", "Capital of France?", "Hello", "Define gravity", "Who is the CEO of Microsoft?",
    "What is the boiling point of water?", "Name a primary color", "What is 5+7?", "What is the opposite of hot?", "What is 10 divided by 2?",
    "Square root of 16?", "Largest planet in solar system?", "Synonym of happy?", "Antonym of cold?", "What is 3*3?",
    "Who wrote Hamlet?", "What is H2O?", "What is 100/10?", "Name a continent", "What is 7+8?",
    "What is 9-4?", "What is 12*12?", "Smallest prime number?", "What is 1+0?", "What is 20/5?",

    # Complex prompts
    "Explain binary search algorithm", "Describe DNA replication", "How does garbage collection work in Java?",
    "Advantages of cloud computing", "Impact of quantum mechanics on AI",
    "Write a SQL query to join two tables", "Explain neural networks", "Describe the theory of relativity",
    "What are the ethical issues in AI?", "Explain blockchain consensus mechanism",
    "Explain recursion with examples", "Describe machine learning pipeline", "How does TCP/IP work?",
    "Explain the process of photosynthesis", "Describe the Big Bang theory",
    "Explain how compilers work", "Describe operating system scheduling", "Explain deep learning vs traditional ML",
    "Explain CRISPR gene editing", "Describe how encryption works",
    "Explain distributed systems", "Describe cloud-native architecture", "Explain reinforcement learning",
    "Explain quantum computing basics", "Describe how search engines index the web"
]

y = [0]*25 + [1]*25  # 0 = simple, 1 = complex


# Build pipeline
model = Pipeline([
    ('vectorizer', CountVectorizer(max_features=500, ngram_range=(1, 2))),
    ('classifier', LogisticRegression())
])

# Train
model.fit(X, y)

# Save
joblib.dump(model, "routing_model.pkl")
print("New routing_model.pkl saved")
