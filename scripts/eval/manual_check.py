import json
import random

data = json.load(open('data/eval/eval_progress.json'))
random.seed(42)
sample_idx = random.sample(range(len(data['question'])), 15)

for i in sample_idx:
    print(f"Q: {data['question'][i]}")
    print(f"A: {data['answer'][i]}")
    print(f"Gold: {data['ground_truth'][i]}")
    print("=" * 60)