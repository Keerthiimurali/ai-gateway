# AI Gateway — Smart LLM Routing System
This project implements a smart AI Gateway that dynamically routes user prompts to the most appropriate language model based on task complexity.
Instead of using a single model for all queries, the system intelligently chooses between a fast model (low cost, low latency) and a capable model (higher reasoning ability).
The goal is to optimize cost, latency, and response quality.

# Models
1) Fast Model: llama-3.1-8b-instant
Used for simple queries, greetings, short answers

2) Capable Model: gemini-2.0-flash (Google AI Studio free tier)
Used for reasoning, coding, and complex tasks

# Features
Intelligent routing model (ML + rule-based)
Cost optimization via selective model usage
Cache layer for repeated prompts
Logging system for transparency
Streamlit log viewer UI

# Architecture
User → Cache → Routing Model → LLM → Response → Logs

Components: FastAPI Gateway, Routing Model, Cache Layer, Log Viewer

# Setup
Clone the repository
git clone <https://github.com/Keerthiimurali/ai-gateway.git>

Create a virtual environment
python -m venv venv

Activate the environment
venv\Scripts\activate  

Install dependencies
pip install -r requirements.txt

Environment setup
Copy .env.example to .env and insert your API keys
GROQ_API_KEY=groq_key_here
GOOGLE_API_KEY=google_key_here

Run the server
uvicorn app:app --reload

Run the log viewer
streamlit run log_viewer.py

# Test Suite
A 20‑prompt test suite file named test_prompts.csv is included in the repository.
Each prompt is labeled as simple or complex for ground‑truth evaluation.

Run the PoC evaluator:
python poc.py

Outputs include per‑prompt prediction, accuracy, false positives, and false negatives.

# PoC — Routing Model Evaluation
Run:
python poc.py

# Outputs:
Per prompt prediction
Accuracy
False positives
False negatives

# Results
Accuracy: 95%
Cost Reduction: ~34%
Cache Hit Rate: ~58%

The system successfully balances cost and quality.

# Failure Cases
Prompt: "How are you?"
Misrouted to Capable instead of Fast
Cause: Question format confused the classifier

Prompt: "Give me the algorithm for binary search"
Misrouted to Fast instead of Capable
Cause: Probability threshold borderline

Prompt: "Summarize the causes of World War II"
Misrouted to Fast instead of Capable
Cause: Length and keyword signals underestimated complexity

# Research Findings
Routing model works effectively with 85% accuracy
Significant cost reduction achieved compared to baseline
Failures occur in borderline prompts
Cache improves efficiency significantly
Future improvements include semantic routing

# Demo
Simple prompt → Fast model
Complex prompt → Capable model
Repeated prompt → Cache hit
PoC evaluation shown

# Conclusion
This project demonstrates that intelligent routing can significantly reduce cost while maintaining response quality, making AI systems more scalable and efficient.