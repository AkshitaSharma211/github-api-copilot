import json
from sentence_transformers import SentenceTransformer
import numpy as np

chunks = json.load(open('data/processed/chunks.json'))
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
embeddings = model.encode([c['text'] for c in chunks], show_progress_bar=True)

print(embeddings.shape)
np.save('data/processed/chunk_embeddings.npy', embeddings)