import re
import os
import json
import nltk
from app.config import settings

# Download NLTK data if not already present
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('stopwords', quiet=True)
    except Exception as e:
        # If download fails, we'll handle it gracefully
        pass

# Use configuration for data directory
DATA_DIR = os.path.join(settings.data_dir, 'tokens')
os.makedirs(DATA_DIR, exist_ok=True)

def tokenize_text(text: str) -> list[str]:
    #lowercase
    text = text.lower()
    #remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    #split into words
    words = text.split(' ')
    
    #remove stopwords if available
    try:
        stopwords = nltk.corpus.stopwords.words('english')
        words = [word for word in words if word not in stopwords]
    except LookupError:
        # If stopwords are not available, continue without filtering
        pass
    
    #remove empty strings
    words = [word for word in words if word != '']
    return words

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
