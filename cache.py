from difflib import SequenceMatcher

# In-memory cache dictionary
cache_store = {}


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# Retrieve from cache if similar prompt exists
def get_from_cache(prompt: str, threshold: float = 0.85):
    for cached_prompt, cached_response in cache_store.items():
        if similarity(prompt, cached_prompt) >= threshold:
            return cached_response, True  # cache hit
    return None, False  # cache miss

# Save response to cache
def save_to_cache(prompt: str, response: dict):
    cache_store[prompt] = response
