import json
import sys
sys.path.append('scripts/retrieval')
from hybrid_search import hybrid_search

golden = json.load(open('data/eval/golden_dataset.json'))

hits = 0
total = 0

for item in golden:
    if item['gold_answer'] == 'NOT_COVERED':
        continue  # skip negatives for retrieval scoring
    total += 1
    results = hybrid_search(item['question'], top_k=5)
    retrieved_urls = [chunk['source_url'] for chunk, score in results]
    if item['source_url'] in retrieved_urls:
        hits += 1

recall_at_5 = hits / total if total > 0 else 0
print(f"Recall@5: {recall_at_5:.2%} ({hits}/{total})")