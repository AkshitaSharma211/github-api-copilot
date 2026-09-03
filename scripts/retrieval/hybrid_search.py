import json
import re
import chromadb
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

STOPWORDS = {
    'a', 'an', 'the', 'is', 'are', 'was', 'were', 'what', 'when', 'where',
    'how', 'does', 'do', 'did', 'i', 'you', 'to', 'of', 'in', 'on', 'for',
    'and', 'or', 'mean', 'getting', 'get', 'with', 'by', 'from'
}

def tokenize(text):
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    return [w for w in words if w not in STOPWORDS]

# --- setup: load everything once ---
chunks = json.load(open('data/processed/chunks.json'))
tokenized = [tokenize(c['text']) for c in chunks]
bm25 = BM25Okapi(tokenized)

client = chromadb.PersistentClient(path='data/processed/chroma_db')
collection = client.get_collection(name='github_api_docs')
model = SentenceTransformer('BAAI/bge-small-en-v1.5')

def bm25_rank(query, k=50):
    scores = bm25.get_scores(tokenize(query))
    top_idx = scores.argsort()[::-1][:k]
    return [chunks[i]['chunk_id'] for i in top_idx]

def vector_rank(query, k=50):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)
    return [int(cid) for cid in results['ids'][0]]

def reciprocal_rank_fusion(bm25_ids, vector_ids, k=60):
    scores = {}
    for rank, cid in enumerate(bm25_ids):
        scores[cid] = scores.get(cid, 0) + 1 / (k + rank + 1)
    for rank, cid in enumerate(vector_ids):
        scores[cid] = scores.get(cid, 0) + 1 / (k + rank + 1)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def hybrid_search(query, top_k=5):
    bm25_ids = bm25_rank(query)
    vector_ids = vector_rank(query)
    fused = reciprocal_rank_fusion(bm25_ids, vector_ids)
    chunk_by_id = {c['chunk_id']: c for c in chunks}
    return [(chunk_by_id[cid], score) for cid, score in fused[:top_k]]

if __name__ == "__main__":
    # find the actual target chunk (the real "Get an issue" endpoint)
    target_id = None
    for c in chunks:
        if c['path'] == '/repos/{owner}/{repo}/issues/{issue_number}' and c['method'] == 'get':
            target_id = c['chunk_id']
            print(f"Target chunk_id: {target_id}")
            break

    query = "What does a 404 mean when getting an issue?"

    # check target's true rank across the FULL corpus, not just top-20
    bm25_full = bm25_rank(query, k=1328)
    vector_full = vector_rank(query, k=1328)
    print("BM25 rank of target:", bm25_full.index(target_id) if target_id in bm25_full else "not found")
    print("Vector rank of target:", vector_full.index(target_id) if target_id in vector_full else "not found")
    print()

    # then show the actual top-5 hybrid results
    results = hybrid_search(query)
    for chunk, score in results:
        print(f"rrf score: {score:.4f}")
        print(f"[chunk_id: {chunk['chunk_id']}] [{chunk['method'].upper()} {chunk['path']}]")
        print(chunk['text'][:300])
        print()