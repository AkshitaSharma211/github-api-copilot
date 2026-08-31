import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path='data/processed/chroma_db')
collection = client.get_collection(name='github_api_docs')
model = SentenceTransformer('BAAI/bge-small-en-v1.5')

query = "What does a 404 mean when getting an issue?"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=5
)
print(results)

for doc, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
    print(f"--- distance: {dist:.4f} ---")
    print(doc[:200])
    print(meta['source_url'])
    print()