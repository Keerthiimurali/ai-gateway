from difflib import SequenceMatcher
import re
from logger import append_log   # ✅ JSON logger (correct as per document)

# In-memory cache
cache_store = {}

# -------------------------------
# STEP 1: Normalize text
# -------------------------------
def normalize(text: str) -> str:
    text = text.lower().strip()

    # -------------------------------
    # STEP 1: Handle greetings
    # -------------------------------
    greeting_map = {
        "hi": "hello",
        "hey": "hello",
        "hello": "hello"
    }

    if text in greeting_map:
        return greeting_map[text]

    # -------------------------------
    # STEP 2: Synonym normalization
    # -------------------------------
    synonym_map = {
        "how does": "explain",
        "how do": "explain",
        "what is": "explain",
        "difference between": "compare"
    }

    for key, value in synonym_map.items():
        text = text.replace(key, value)

    # -------------------------------
    # STEP 3: Fix common typos
    # -------------------------------
    text = text.replace("pragramming", "programming")

    # -------------------------------
    # STEP 4: Clean text
    # -------------------------------
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)

    return text.strip()

# -------------------------------
# STEP 2: Similarity function
# -------------------------------
def similarity(a: str, b: str) -> float:
    # Word-based similarity (better than character-based)
    set_a = set(a.split())
    set_b = set(b.split())

    if not set_a or not set_b:
        return 0.0

    return len(set_a & set_b) / len(set_a | set_b)

# -------------------------------
# STEP 3: Retrieve BEST match
# -------------------------------
def get_from_cache(prompt: str, threshold: float = 0.65):
    prompt_norm = normalize(prompt)

    best_score = 0
    best_response = None
    best_prompt = None

    for cached_prompt, cached_response in cache_store.items():
        cached_norm = normalize(cached_prompt)
        score = similarity(prompt_norm, cached_norm)

        # Debug print (for demo/understanding)
        print(f"Similarity: '{prompt}' vs '{cached_prompt}' = {score:.2f}")

        if score > best_score:
            best_score = score
            best_response = cached_response
            best_prompt = cached_prompt

    # -------------------------------
    # CACHE HIT
    # -------------------------------
    if best_score >= threshold:
        print(f"Cache HIT (score={best_score:.2f}) using: '{best_prompt}'")

        append_log({
            "event": "cache_hit",
            "input": prompt,
            "matched_prompt": best_prompt,
            "similarity_score": round(best_score, 2),
            "cache_hit": True
        })

        return best_response, True, best_score

    # -------------------------------
    # CACHE MISS
    # -------------------------------
    print(f"Cache MISS (best_score={best_score:.2f})")

    append_log({
        "event": "cache_miss",
        "input": prompt,
        "similarity_score": round(best_score, 2),
        "cache_hit": False
    })

    return None, False, best_score


# -------------------------------
# STEP 4: Save to cache
# -------------------------------
def save_to_cache(prompt: str, response: str):
    cache_store[prompt] = response

    append_log({
        "event": "cache_save",
        "input": prompt
    })