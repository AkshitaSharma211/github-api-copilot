import json
import os
from dotenv import load_dotenv

load_dotenv()

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.run_config import RunConfig
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_cerebras import ChatCerebras


cerebras_llm = LangchainLLMWrapper(
    ChatCerebras(model="gpt-oss-120b", api_key=os.environ.get('CEREBRAS_API_KEY'))
)


local_embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
)

run_config = RunConfig(
    timeout=180,
    max_workers=1,
    max_retries=5,
    max_wait=90
)

eval_data = json.load(open('data/eval/eval_progress.json'))
dataset = Dataset.from_dict(eval_data)

print(f"Running RAGAS on {len(eval_data['question'])} questions using Groq as judge...")

scores = evaluate(
    dataset,
    metrics=[faithfulness, context_precision, context_recall],
    llm=cerebras_llm,
    embeddings=local_embeddings,
    run_config=run_config
)

print(scores)

with open('data/eval/ragas_results.json', 'w') as f:
    json.dump(dict(scores), f, indent=2)

print("Saved to data/eval/ragas_results.json")