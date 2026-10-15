import re
import os
import json
from app.config import settings

# Deterministic, offline tokenizer: no downloads or filesystem work at import time.
STOPWORDS = frozenset("a an the and or of to in is it for on with as by are be that this from at should".split())
DATA_DIR = os.path.join(settings.data_dir, 'tokens')

def tokenize_text(text: str) -> list[str]:
    return [word for word in re.findall(r"[^\W_]+", text.lower()) if word not in STOPWORDS]

def doc_to_tokens(doc: str) -> list[str]:
    #open doc and read text
    with open(doc, "r") as f:
        doc_json = json.load(f)
        #tokenize each sentence
        tokens = tokenize_text(doc_json["text"])
        token_doc = {
            "id": doc_json["id"],
            "url": doc_json["url"],
            "title": doc_json["title"],
            "text": tokens,
        }
        return token_doc

def tokenize_docs(docs: list[str]) -> list[str]:
    os.makedirs(DATA_DIR, exist_ok=True)
    #tokenize each doc
    token_docs = []
    for doc in docs:
        token_doc = doc_to_tokens(doc)
        token_docs.append(token_doc)
        with open(os.path.join(DATA_DIR, f"{token_doc['id']}.json"), "w", encoding="utf-8") as f:
            json.dump(token_doc, f, ensure_ascii=False, indent=2)
    return token_docs

if __name__ == "__main__":
    list_of_docs = ['../../../data/docs/0.json', '../../../data/docs/1.json', '../../../data/docs/2.json', '../../../data/docs/3.json', '../../../data/docs/4.json']
    token_docs = tokenize_docs(list_of_docs)
    print(f"Tokenized {len(token_docs)} docs")
