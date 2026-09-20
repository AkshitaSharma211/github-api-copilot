import json
import sys
import time
sys.path.append('scripts/retrieval')
from generate import answer as rag_answer

golden = json.load(open('data/eval/golden_dataset.json'))
negatives = [g for g in golden if g['gold_answer'] == 'NOT_COVERED']


def safe_rag_answer(question, retries=3):
    for attempt in range(retries):
        try:
            return rag_answer(question)
        except Exception as e:
            print(f"Retry {attempt+1} for: {question[:50]}... ({e})")
            time.sleep(10)
    return {"answer": "ERROR: failed after retries", "source_url": []}

correct_refusals = 0
for item in negatives:
    result = safe_rag_answer(item['question'])
    time.sleep(2)
    if "isn't covered" in result['answer'].lower():
        correct_refusals += 1
    else:
        print(f"MISSED REFUSAL: {item['question']}")
        print(f"Got: {result['answer']}\n")

print(f"Correct refusals: {correct_refusals}/{len(negatives)}")