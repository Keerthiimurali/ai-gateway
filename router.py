from fastapi import APIRouter
from pydantic import BaseModel
from routing import routing_model
from cache import get_from_cache, save_to_cache
from logger import append_log
from models import call_fast_model, call_capable_model
from cost import calculate_cost_inr
import time

router = APIRouter()

# -------------------------------
# Request & Response Models
# -------------------------------
class ChatRequest(BaseModel):
    prompt: str

class Metadata(BaseModel):
    prompt: str
    model_used: str
    routing_reason: str
    confidence: float
    latency: float
    cache_hit: bool
    similarity_score: float
    tokens_used: int
    cost_inr: float
    signals: list

class ChatResponse(BaseModel):
    response: str
    metadata: Metadata

# -------------------------------
# Endpoint
# -------------------------------
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    prompt = request.prompt
    start_time = time.time()

    # STEP 1: CACHE CHECK
    cached_response, cache_hit, similarity_score = get_from_cache(prompt)

    if cache_hit:
        latency = round(time.time() - start_time, 3)
        log_entry = {
            "prompt": prompt[:50],
            "model_used": "cache",
            "routing_reason": f"Cache hit (similarity={similarity_score:.2f})",
            "confidence": 1.0,
            "latency": latency,
            "cache_hit": True,
            "similarity_score": similarity_score,
            "tokens_used": 0,
            "cost_inr": 0.0,
            "signals": []
        }
        append_log(log_entry)
        return {"response": cached_response, "metadata": log_entry}

    # STEP 2: ROUTING MODEL
    decision, reason, confidence, signals = routing_model(prompt)

    # STEP 3: MODEL CALL
    if decision == "fast":
        response_text, tokens = call_fast_model(prompt)
    else:
        response_text, tokens = call_capable_model(prompt)

    latency = round(time.time() - start_time, 3)

    # STEP 4: COST CALCULATION
    cost_inr = calculate_cost_inr(decision, tokens)

    # STEP 5: CACHE SAVE
    save_to_cache(prompt, response_text)

    # STEP 6: LOGGING
    log_entry = {
        "prompt": prompt[:50],
        "model_used": decision,
        "routing_reason": reason,
        "confidence": confidence,
        "latency": latency,
        "cache_hit": False,
        "similarity_score": similarity_score,
        "tokens_used": tokens,
        "cost_inr": cost_inr,
        "signals": signals
    }
    append_log(log_entry)

    return {"response": response_text, "metadata": log_entry}
