# backend/scripts/build_index.py

import os
import json
import redis
from app.utilts.tokenizer import tokenize_docs
from app.index.tfidf_indexer import build_tf_idf
from app.index.inverted_index import build_inverted_index, load_tokenized_docs, save_index

r = redis.Redis()

DOC_PATH = "../../data/docs"
TOKEN_PATH = "../../data/tokens"

def rebuild_index():
    print("[INFO] Rebuilding index...")

    # Step 1: Tokenize
    doc_files = [os.path.join(DOC_PATH, f) for f in os.listdir(DOC_PATH)]
    tokenize_docs(doc_files)

    # Step 2: Build index by tfidf and inverted index
    docs = load_tokenized_docs()
    inverted_index = build_inverted_index(docs)
    save_index(inverted_index)
    tfidf_index, df = build_tf_idf()

    # Step 3: Store in Redis
    for term, postings in tfidf_index.items():
        r.delete(f"tfidf:{term}")
        r.hset(f"tfidf:{term}", mapping=postings)

    for term, freq in df.items():
        r.set(f"df:{term}", freq)
    # Filter out terms that are empty
    filtered = [(term, freq) for term, freq in df.items() if term != '']

    # Sort by frequency descending
    top_ten_frequent_terms = sorted(filtered, key=lambda x: x[1], reverse=True)[:10]
    top_ten_frequent_terms_inverted_index = sorted(inverted_index.items(), key=lambda x: len(x[1]), reverse=True)[:10]

    print("[DONE] Index rebuilt!")
    print(f"Top ten frequent terms TFIDF: {top_ten_frequent_terms}")
    print(f"Top ten frequent terms Inverted Index: {top_ten_frequent_terms_inverted_index}")
    return top_ten_frequent_terms, top_ten_frequent_terms_inverted_index

