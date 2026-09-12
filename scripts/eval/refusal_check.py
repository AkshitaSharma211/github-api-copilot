import json
import sys
import time
sys.path.append('scripts/retrieval')
from generate import answer as rag_answer

golden = json.load(open('data/eval/golden_dataset.json'))
negatives = [g for g in golden if g['gold_answer'] == 'NOT_COVERED']

correct_refusals = 0
for item in negatives:
    result = rag_answer(item['question'])
    time.sleep(2)
    if "doesn't cover" in result['answer'].lower():
        correct_refusals += 1
    else:
        print(f"MISSED REFUSAL: {item['question']}")
        print(f"Got: {result['answer']}\n")

print(f"Correct refusals: {correct_refusals}/{len(negatives)}")