import json
import numpy as np
import chromadb

chunks = json.load(open('data/processed/chunks.json'))
embeddings = np.load('data/processed/chunk_embeddings.npy')

client = chromadb.PersistentClient(path='data/processed/chroma_db')
try:
    client.delete_collection(name='github_api_docs')
except Exception:
    pass

collection = client.create_collection(name='github_api_docs')

collection.add(
    ids=[str(c['chunk_id']) for c in chunks],
    embeddings=embeddings.tolist(),
    documents=[c['text'] for c in chunks],
    metadatas=[{'path': c['path'], 'method': c['method'], 'source_url': c['source_url']} for c in chunks]
)

print(collection.count())