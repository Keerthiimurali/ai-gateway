from fastapi import APIRouter
from routing import routing_model
from cache import get_from_cache, save_to_cache
from logger import append_log
from models import call_fast_model, call_capable_model
import time
from datetime import datetime

router = APIRouter()

@router.post("/chat")
def chat(prompt: str):
    start_time = time.time()

    #Step 1: Cache check
    cached_response, cache_hit = get_from_cache(prompt)
    if cache_hit:
        latency = round(time.time() - start_time, 3)

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prompt": prompt[:50],
            "model_used": "cache",
            "routing_reason": "Returned from cache",
            "confidence": 1.0,
            "latency": latency,
            "cache_hit": True,
            "tokens_used": 0
        }

        append_log(log_entry)

        return {
            "response": cached_response,
            "metadata": log_entry
        }

    #Step 2: Routing decision
    decision, reason, confidence = routing_model(prompt)

    #Step 3: Model call
    if decision == "fast":
        response_text, tokens = call_fast_model(prompt)
    else:
        response_text, tokens = call_capable_model(prompt)

    latency = round(time.time() - start_time, 3)

    #Step 4: Cache save
    save_to_cache(prompt, response_text)

    #Step 5: Logging
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prompt": prompt[:50],
        "model_used": decision,
        "routing_reason": reason,
        "confidence": confidence,
        "latency": latency,
        "cache_hit": False,
        "tokens_used": tokens
    }

    append_log(log_entry)

    return {
        "response": response_text,
        "metadata": log_entry
    }