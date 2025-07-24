import os, json
import redis

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
TOKEN_PATH = os.path.join(BASE, '../data/tokens')
DOC_PATH = os.path.join(BASE, '../data/docs')
TFIDF_PATH = os.path.join(BASE, '../index/tfidf_index.json')
DF_PATH = os.path.join(BASE, '../index/doc_freq.json')

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Store TF-IDF index
with open(TFIDF_PATH) as f:
    tfidf_index = json.load(f)
    for term, postings in tfidf_index.items():
        r.hset(f"tfidf:{term}", mapping=postings)

# Store DF
with open(DF_PATH) as f:
    df = json.load(f)
    for term, freq in df.items():
        r.set(f"df:{term}", freq)

# Store tokenized docs and metadata
for fname in os.listdir(TOKEN_PATH):
    with open(os.path.join(TOKEN_PATH, fname)) as f:
        tok = json.load(f)
        doc_id = tok["id"]
        r.set(f"tokens:{doc_id}", json.dumps(tok["text"]))
        r.set(f"title:{doc_id}", tok["title"])
        r.sadd("docs", doc_id)

# Store full docs
for fname in os.listdir(DOC_PATH):
    with open(os.path.join(DOC_PATH, fname)) as f:
        doc = json.load(f)
        r.set(f"doc:{doc['id']}", json.dumps(doc))
