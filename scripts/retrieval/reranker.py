from sentence_transformers import CrossEncoder
from hybrid_search import hybrid_search, bm25_rank, vector_rank, reciprocal_rank_fusion, chunks

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_search(query, candidate_k=20, final_k=5):
    # get a wider hybrid candidate pool first
    bm25_ids = bm25_rank(query, k=candidate_k)
    vector_ids = vector_rank(query, k=candidate_k)
    fused = reciprocal_rank_fusion(bm25_ids, vector_ids)
    chunk_by_id = {c['chunk_id']: c for c in chunks}
    candidates = [chunk_by_id[cid] for cid, score in fused[:candidate_k]]

    # score each (query, chunk) pair with the cross-encoder
    pairs = [[query, c['text']] for c in candidates]
    scores = reranker.predict(pairs)

    # sort candidates by cross-encoder score, take final_k
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return ranked[:final_k]

if __name__ == "__main__":
    queries = [
        "What does a 404 mean when getting an issue?",
        "What are the required path parameters to get a single issue?",  # more specific, less ambiguous
    ]
    for query in queries:
        print(f"=== QUERY: {query} ===")
        results = rerank_search(query)
        for chunk, score in results:
            print(f"cross-encoder score: {score:.4f}")
            print(f"[chunk_id: {chunk['chunk_id']}] [{chunk['method'].upper()} {chunk['path']}]")
            print(chunk['text'][:200])
            print()