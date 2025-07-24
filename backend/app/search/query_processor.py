import os
import json
from collections import defaultdict
from typing import List, Dict
from app.utilts.tokenizer import tokenize_text
import redis

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
TFIDF_PATH = os.path.join(BASE_DIR, '../index/tfidf_index.json')
DOC_PATH = os.path.join(BASE_DIR, '../data/tokens')

with open(TFIDF_PATH, "r") as f:
    tfidf_index = json.load(f)

def load_docs():
    docs = {}
    for fname in os.listdir(DOC_PATH):
        with open(os.path.join(DOC_PATH, fname)) as f:
            doc = json.load(f)
            docs[doc["id"]] = doc
    return docs

docs = load_docs()

def generate_snippet(doc, terms):
    full_path = os.path.join(DOC_PATH.replace("/tokens", "/docs"), f"{doc['id']}.json")
    with open(full_path) as f:
        original = json.load(f)["text"]
    for term in terms:
        if term in original:
            idx = original.lower().index(term)
            start = max(0, idx - 50)
            end = min(len(original), idx + 50)
            return original[start:end] + "..."
    return original[:100] + "..."

def search(query: str, op: str = "AND") -> List[Dict]:
    tokens = tokenize_text(query)
    scores = defaultdict(float)
    doc_sets = []

    for token in tokens:
        if token in tfidf_index:
            doc_sets.append(set(tfidf_index[token].keys()))
            for doc_id, score in tfidf_index[token].items():
                scores[doc_id] += score

    if not doc_sets:
        return []

    if op == "AND":
        matched_docs = set.intersection(*doc_sets)
    elif op == "OR":
        matched_docs = set.union(*doc_sets)
    elif op == "NOT":
        all_docs = set(docs.keys())
        matched_docs = all_docs - set.union(*doc_sets)
    else:
        matched_docs = set.union(*doc_sets)

    # Return top 10 sorted by TF-IDF score
    ranked = sorted(matched_docs, key=lambda d: scores[str(d)], reverse=True)
    

    results = []
    for doc_id in ranked[:10]:
        doc = docs[int(doc_id)]
        snippet = generate_snippet(doc, tokens)
        results.append({
            "id": doc["id"],
            "title": doc["title"],
            "url": doc["url"],
            "snippet": snippet
        })
    return results

