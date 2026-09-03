import json
import re
from rank_bm25 import BM25Okapi

STOPWORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'what', 'when', 'where',
    'how', 'does', 'do', 'did', 'i', 'you', 'to', 'of', 'in', 'on', 'for',
    'and', 'or', 'mean', 'getting', 'get', 'with', 'by', 'from'
}

def tokenize(text):
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    return [w for w in words if w not in STOPWORDS]

chunks = json.load(open('data/processed/chunks.json'))
tokenized = [tokenize(c['text']) for c in chunks]
bm25 = BM25Okapi(tokenized)

def bm25_search(query, k=5):
    scores = bm25.get_scores(tokenize(query))
    top_idx = scores.argsort()[::-1][:k]
    return [(chunks[i], scores[i]) for i in top_idx]

if __name__ == "__main__":
    results = bm25_search("What does a 404 mean when getting an issue?")
    for chunk, score in results:
        print(f"score: {score:.2f}")
        print(chunk['text'][:400])
        print()