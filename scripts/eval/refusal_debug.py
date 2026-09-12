import json
import sys
import time
sys.path.append('scripts/retrieval')
from generate import answer as rag_answer

golden = json.load(open('data/eval/golden_dataset.json'))
negatives = [g for g in golden if g['gold_answer'] == 'NOT_COVERED']

for item in negatives:
    result = rag_answer(item['question'])
    time.sleep(5)
    print(f"Q: {item['question']}")
    print(f"A: {result['answer']}")
    print(f"Sources: {result['source_url']}")
    print("=" * 60)