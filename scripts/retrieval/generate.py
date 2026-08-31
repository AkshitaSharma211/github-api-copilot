import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = chromadb.PersistentClient(path='data/processed/chroma_db')
collection = client.get_collection(name='github_api_docs')
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def retrieve(query, k=5):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)
    return list(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ))

def build_prompt(query, chunks):
    context = ""
    for i, (doc, meta, dist) in enumerate(chunks):
        context += f"[Source {i+1}] {doc}\n(URL: {meta['source_url']})\n\n"

    prompt = f"""Answer the question using ONLY the context below. Cite the source URL for every claim you make, in the format [Source URL].
If the context doesn't contain the answer, say so — do not make anything up.

Context:
{context}

Question: {query}

Answer:"""
    return prompt

def answer(query, k=5):
    chunks = retrieve(query, k)
    prompt = build_prompt(query, chunks)
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    q = "What does a 404 mean when getting an issue?"
    print(answer(q))