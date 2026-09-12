import json
import sys
import time
sys.path.append('scripts/retrieval')
from generate import answer as rag_answer, retrieve

from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from datasets import Dataset

golden = json.load(open('data/eval/golden_dataset.json'))
golden = [g for g in golden if g['gold_answer'] != 'NOT_COVERED']  # RAGAS needs real ground truth

eval_data = {"question": [], "answer": [], "contexts": [], "ground_truth": []}

for item in golden:
    result = rag_answer(item['question'])
    time.sleep(5)
    chunks = retrieve(item['question'])
    eval_data["question"].append(item['question'])
    eval_data["answer"].append(result['answer'])
    eval_data["contexts"].append([c[0] for c in chunks])
    eval_data["ground_truth"].append(item['gold_answer'])

dataset = Dataset.from_dict(eval_data)
scores = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
print(scores)

with open('data/eval/ragas_results.json', 'w') as f:
    json.dump(dict(scores), f, indent=2)