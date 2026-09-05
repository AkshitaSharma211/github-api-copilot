import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
import sys
from dotenv import load_dotenv
load_dotenv()

client = chromadb.PersistentClient(path='data/processed/chroma_db')
collection = client.get_collection(name='github_api_docs')
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

sys.path.append(os.path.join(os.path.dirname(__file__)))
from reranker import rerank_search

def retrieve(query, k=5):
    results = rerank_search(query, final_k=k)
    return [(chunk['text'], {'source_url': chunk['source_url']}, score) for chunk, score in results]

def build_prompt(query, chunks):
    context = ""
    for i, (doc, meta, dist) in enumerate(chunks):
        context += f"[Source {i+1}] {doc}\n(URL: {meta['source_url']})\n\n"

    prompt = f"""You are answering a developer's question about the GitHub REST API using ONLY the context below.

FORMAT RULES — follow exactly, every time:
- Write in plain prose sentences. No markdown tables, no bullet lists, no bold/asterisks, unless the question specifically asks for a list of parameters or options — only then use a simple "- " bullet list.
- Keep the answer to 2-4 sentences unless the question genuinely requires more detail to be correct.
- After each claim, cite its source inline in this EXACT format and nothing else: (Source: <full URL>)
- Do not use numbered references like [1] or [Source 2]. Do not add a separate "Sources:" section at the end. Every citation must be the full URL, inline, in parentheses, right after the claim it supports.
- If the context does not contain the answer, say plainly: "The provided context doesn't cover this." Do not guess.

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
    test_questions = [
    # Basic endpoint lookup
    "What does the endpoint for getting a single issue do?",
    "How do I create a new issue in a repository?",
    "What endpoint do I use to list pull requests for a repo?",
    "How can I get information about a repository's collaborators?",
    "What does the 'list issues assigned to the authenticated user' endpoint return?",

    # Error codes / exact-term matching
    "What does a 404 mean when getting an issue?",
    "What does a 403 error mean when creating an issue?",
    "When would I get a 410 status code from the issues API?",
    "What does a 422 error mean when creating a repository?",
    "What is a 301 response when fetching an issue?",

    # Parameters
    "What parameters does the list issues endpoint accept?",
    "What does the 'state' query parameter do for listing issues?",
    "Is the issue_number a path parameter or a query parameter?",
    "What parameters are required to get a single issue?",

    # No good answer in corpus (tests hallucination resistance)
    "How do I authenticate using OAuth device flow?",
    "What's GitHub's rate limit for the search API?",
    "How do I use GitHub Actions to deploy to AWS?",

    # Loosely-phrased / real-user style
    "Why is my push getting blocked?",
    "My API call for an issue isn't working, what's wrong?",
    "How do I see who's assigned to my issues?",
]
    for q in test_questions:
        print(f"Q: {q}")
        print(answer(q))
        print("=" * 80)