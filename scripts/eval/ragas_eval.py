import json
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append('scripts/retrieval')
from generate import answer as rag_answer, retrieve

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from langchain_google_genai import ChatGoogleGenerativeAI

gemini_llm = LangchainLLMWrapper(ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.environ.get('GEMINI_API_KEY')))

golden = json.load(open('data/eval/golden_dataset.json'))
golden = [g for g in golden if g['gold_answer'] != 'NOT_COVERED']

eval_data = {"question": [], "answer": [], "contexts": [], "ground_truth": []}

def safe_rag_answer(question, retries=3):
    for attempt in range(retries):
        try:
            return rag_answer(question)
        except Exception as e:
            print(f"Retry {attempt+1} for: {question[:50]}... ({e})")
            time.sleep(15)
    return {"answer": "ERROR: failed after retries", "source_url": []}

for item in golden:
    result = safe_rag_answer(item['question'])
    time.sleep(5)
    chunks = retrieve(item['question'])
    eval_data["question"].append(item['question'])
    eval_data["answer"].append(result['answer'])
    eval_data["contexts"].append([c[0] for c in chunks])
    eval_data["ground_truth"].append(item['gold_answer'])

dataset = Dataset.from_dict(eval_data)
scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall], llm=gemini_llm)
print(scores)

with open('data/eval/ragas_results.json', 'w') as f:
    json.dump(dict(scores), f, indent=2)