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

def retrieve(query, k=5):
    results = hybrid_search(query, top_k=k)
    return [(chunk['text'], {'source_url': chunk['source_url']}, score) for chunk, score in results]

def build_prompt(query, chunks):
    context = ""
    for i, (doc, meta, dist) in enumerate(chunks):
        context += f"[Source {i+1}] {doc}\n(URL: {meta['source_url']})\n\n"

    with open('configs/prompts/v1.txt') as f:
        template = f.read()

    return template.format(context=context, query=query)

def answer(query, k=5):
    chunks = retrieve(query, k)
    prompt = build_prompt(query, chunks)

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0

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