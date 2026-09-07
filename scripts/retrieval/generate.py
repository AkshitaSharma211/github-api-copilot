import os
import sys
import json
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
from hybrid_search import hybrid_search


load_dotenv()

client = chromadb.PersistentClient(path='data/processed/chroma_db')
collection = client.get_collection(name='github_api_docs')
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

sys.path.append(os.path.join(os.path.dirname(__file__)))
from reranker import rerank_search

def retrieve(query, k=5):
    results = hybrid_search(query, top_k=k)
    return [(chunk['text'], {'source_url': chunk['source_url']}, score) for chunk, score in results]

def build_prompt(query, chunks):
    context = ""
    for i, (doc, meta, dist) in enumerate(chunks):
        context += f"[Source {i+1}] {doc}\n(URL: {meta['source_url']})\n\n"

    prompt = f"""You are answering a developer's question about the GitHub REST API using ONLY the context below.

FORMAT RULES — follow exactly, every time:
- Write in plain prose sentences. No markdown tables, no bullet lists, no bold/asterisks, unless the question specifically asks for a list of parameters or options — only then use a simple "- " bullet list.
- Keep the answer to 2-4 sentences unless the question genuinely requires more detail to be correct.
- If the context does not contain the answer, say plainly: "The provided context doesn't cover this." Do not guess.

Respond with ONLY a valid JSON object, nothing else before or after it — no markdown code fences, no explanation outside the JSON.
Use exactly this shape:
{{
  "answer": "<your answer here, following the content rules above>",
  "source_url": ["<url1>", "<url2>", ...]
}}
Include every source URL (copied exactly from the context above, character-for-character) that a claim in your answer actually depends on. Do not include a URL that isn't in the context. If your answer relies on only one source, source_url should still be a list with one item in it.

Context:
{context}

Question: {query}
"""
    return prompt

def answer(query, k=5):
    chunks = retrieve(query, k)
    prompt = build_prompt(query, chunks)

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    raw = response.choices[0].message.content
    print("RAW MODEL OUTPUT:", raw)  

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {"answer": "Error: model did not return valid JSON.", "source_url": [], "raw": raw}

    model_answer = parsed.get("answer", "")
    model_sources = parsed.get("source_url", [])

    # validate citations against what was actually retrieved
    real_urls = {meta['source_url'] for _, meta, _ in chunks}
    hallucinated = [u for u in model_sources if u not in real_urls]

    if hallucinated:
        print(f"WARNING: hallucinated citation(s) not in retrieved context: {hallucinated}")

    return {
        "answer": model_answer,
        "source_url": model_sources,
        "hallucinated_citations": hallucinated
    }

if __name__ == "__main__":
    test_questions = [
        "What does the endpoint for getting a single issue do?",
        "How do I create a new issue in a repository?",
        "What does a 404 mean when getting an issue?",
        "What does a 403 error mean when creating an issue?",
        "What parameters are required to get a single issue?",
        "How do I authenticate using OAuth device flow?",
    ]
    for q in test_questions:
        print(f"Q: {q}")
        result = answer(q)
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['source_url']}")
        if result.get('hallucinated_citations'):
            print(f"⚠️  Hallucinated: {result['hallucinated_citations']}")
        print("=" * 80)