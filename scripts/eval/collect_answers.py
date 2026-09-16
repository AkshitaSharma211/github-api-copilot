import json
import sys
import time
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.append('scripts/retrieval')
from generate import answer as rag_answer, retrieve

CHECKPOINT_FILE = 'data/eval/eval_progress.json'

golden = json.load(open('data/eval/golden_dataset.json'))
golden = [g for g in golden if g['gold_answer'] != 'NOT_COVERED']

# load existing progress if it exists
if os.path.exists(CHECKPOINT_FILE):
    eval_data = json.load(open(CHECKPOINT_FILE))
    done_questions = set(eval_data['question'])
    print(f"Resuming — {len(done_questions)} already done")
else:
    eval_data = {"question": [], "answer": [], "contexts": [], "ground_truth": []}
    done_questions = set()

def safe_rag_answer(question, retries=2):
    for attempt in range(retries):
        try:
            return rag_answer(question)
        except Exception as e:
            print(f"Retry {attempt+1} for: {question[:50]}... ({e})")
            time.sleep(20)
    return None  # signal total failure, don't fake a result

for item in golden:
    if item['question'] in done_questions:
        continue  # skip already-completed questions

    result = safe_rag_answer(item['question'])
    if result is None:
        print(f"STOPPING — hit persistent failure (likely daily limit) at: {item['question'][:50]}")
        break  # stop cleanly instead of crashing, progress is already saved

    chunks = retrieve(item['question'])
    eval_data["question"].append(item['question'])
    eval_data["answer"].append(result['answer'])
    eval_data["contexts"].append([c[0] for c in chunks])
    eval_data["ground_truth"].append(item['gold_answer'])

    # save progress after EVERY question, not just at the end
    json.dump(eval_data, open(CHECKPOINT_FILE, 'w'))
    time.sleep(5)

print(f"\nCompleted so far: {len(eval_data['question'])}/{len(golden)}")