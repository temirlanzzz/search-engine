import redis
from app.utilts.tokenizer import tokenize_text
import json
# Redis connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def search_redis_query(query: str, op="AND") -> list[dict]:
    tokens = tokenize_text(query)
    scores = {}
    doc_sets = []

    for token in tokens:
        tfidf_postings = r.hgetall(f"tfidf:{token}")
        doc_sets.append(set(tfidf_postings.keys()))
        for doc_id, score in tfidf_postings.items():
            scores[doc_id] = scores.get(doc_id, 0) + float(score)

    if not doc_sets:
        return []

    # Combine based on op
    if op == "AND":
        matched = set.intersection(*doc_sets)
    elif op == "OR":
        matched = set.union(*doc_sets)
    elif op == "NOT":
        all_docs = r.smembers("docs")
        matched = set(all_docs) - set.union(*doc_sets)
    else:
        matched = set.union(*doc_sets)

    # Sort by TF-IDF score
    ranked = sorted(matched, key=lambda d: scores.get(d, 0), reverse=True)
    results = []
    for doc_id in ranked[:10]:
        title = r.get(f"title:{doc_id}")

        doc_json = r.get(f"doc:{doc_id}")
        url = json.loads(doc_json)["url"] if doc_json else None

        snippet_raw = r.get(f"tokens:{doc_id}")
        snippet = snippet_raw[:100] + "..." if snippet_raw else "Snippet not available"

        results.append({
            "id": doc_id,
            "title": title,
            "url": url,
            "snippet": snippet
        })

    return results
