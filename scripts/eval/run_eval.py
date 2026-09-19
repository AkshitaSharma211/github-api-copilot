"""
Custom faithfulness / context_precision / context_recall judge.

Why this exists instead of RAGAS's evaluate():
- RAGAS's answer_relevancy needs n>1 completions per call -> Groq hard-rejects n>1.
  We just don't compute answer_relevancy this way. (Optional cheap substitute at the bottom.)
- RAGAS's internal concurrency ignores max_workers in practice and blows through
  Groq's TPM limit mid-run, and a crash mid-run loses everything.
  This script makes exactly ONE call at a time, sleeps between calls, and writes
  each result to disk immediately -> a crash at call 80 loses nothing before call 80.

Usage:
  1. Fill in `load_dataset()` to match your actual data (see the shape described below).
  2. Set GROQ_API_KEY in your environment.
  3. Run: python run_eval.py
  4. If it dies partway (rate limit, network, whatever), just run it again — it
     skips rows already present in results.jsonl and continues.

Expected per-question shape (one dict per question), from your existing RAG eval data:
{
  "question": str,
  "answer": str,              # your RAG system's generated answer
  "contexts": [str, ...],     # the retrieved chunks used to generate the answer
  "ground_truth": str,        # the gold answer (for context_recall)
}
Adjust `load_dataset()` below to actually read this out of your existing files
(e.g. your golden dataset JSON + your saved RAG run outputs, joined on question id).
"""

import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # reads GROQ_API_KEY (and anything else) out of your .env file automatically

from groq import Groq

MODEL = "qwen/qwen3.8-27b"          # different provider family from openai/gpt-oss-20b,
                                      # so it has its own separate daily quota
SLEEP_SECONDS = 6                  # raised from 2.5 — 4000 TPM/min budget needs more room per call
MAX_RETRIES_PER_QUESTION = 3
RESULTS_PATH = Path("results.jsonl")
CLIENT = Groq(api_key=os.environ["GROQ_API_KEY"])


# ---------------------------------------------------------------------------
# 1. DATA LOADING — edit this to match your actual files
# ---------------------------------------------------------------------------
def load_dataset():
    """
    Reads data/eval/eval_progress.json, which is stored column-wise:
    {"question": [...], "answer": [...], "contexts": [...], "ground_truth": [...]}
    Converts it to the row-wise list of dicts the judge functions expect.
    """
    with open("data/eval/eval_progress.json") as f:
        cols = json.load(f)

    n = len(cols["question"])
    rows = []
    for i in range(n):
        rows.append({
            "question": cols["question"][i],
            "answer": cols["answer"][i],
            "contexts": cols["contexts"][i],
            "ground_truth": cols["ground_truth"][i],
        })
    return rows


# ---------------------------------------------------------------------------
# 2. JUDGE PROMPTS — each does ONE scalar judgment, n=1, strict JSON out
# ---------------------------------------------------------------------------
def _call_judge(system_prompt: str, user_prompt: str) -> dict:
    resp = CLIENT.chat.completions.create(
        model=MODEL,
        n=1,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return json.loads(resp.choices[0].message.content)


def judge_faithfulness(answer: str, contexts: list[str]) -> dict:
    """Is every claim in the answer actually supported by the retrieved contexts?"""
    system = (
        "You are a strict fact-checker. Given a set of context passages and an "
        "answer, determine whether the answer's claims are ALL supported by the "
        "context. Respond ONLY with JSON: "
        '{"score": <0.0-1.0>, "unsupported_claims": [<short strings>]}. '
        "score = fraction of claims that are supported. Empty list if fully supported."
    )
    user = f"CONTEXTS:\n{json.dumps(contexts)}\n\nANSWER:\n{answer}"
    return _call_judge(system, user)


def judge_context_precision(question: str, contexts: list[str]) -> dict:
    """Of the retrieved contexts, how many are actually relevant to the question?"""
    system = (
        "You judge retrieval precision. Given a question and a list of retrieved "
        "passages, mark each passage relevant or not. Respond ONLY with JSON: "
        '{"relevant_flags": [<true/false per passage, same order>], '
        '"precision": <0.0-1.0 fraction relevant>}.'
    )
    user = f"QUESTION:\n{question}\n\nPASSAGES:\n{json.dumps(contexts)}"
    return _call_judge(system, user)


def judge_context_recall(ground_truth: str, contexts: list[str]) -> dict:
    """Does the retrieved context set contain enough info to derive the gold answer?"""
    system = (
        "You judge retrieval recall. Given a gold reference answer and a set of "
        "retrieved passages, determine what fraction of the claims in the gold "
        "answer can be attributed to the retrieved passages. Respond ONLY with JSON: "
        '{"score": <0.0-1.0>, "missing_claims": [<short strings>]}.'
    )
    user = f"GOLD ANSWER:\n{ground_truth}\n\nPASSAGES:\n{json.dumps(contexts)}"
    return _call_judge(system, user)


def _judge_with_retry(judge_fn, *args):
    """Retry on rate-limit (429) with a real wait; give up after MAX_RETRIES_PER_QUESTION."""
    last_err = None
    for attempt in range(MAX_RETRIES_PER_QUESTION):
        try:
            return judge_fn(*args)
        except Exception as e:
            last_err = e
            msg = str(e)
            if "429" in msg or "rate_limit" in msg:
                wait = 15 * (attempt + 1)  # 15s, 30s, 45s
                print(f"    rate limited, waiting {wait}s (attempt {attempt+1})")
                time.sleep(wait)
            else:
                # non-rate-limit error (e.g. bad JSON from model) — one quick retry, then give up
                time.sleep(2)
    raise last_err


# ---------------------------------------------------------------------------
# 3. RUNNER — sequential, checkpointed, resumable
# ---------------------------------------------------------------------------
def already_done_ids() -> set:
    """Only questions that SUCCEEDED count as done. Errored rows get retried."""
    if not RESULTS_PATH.exists():
        return set()
    done = set()
    with open(RESULTS_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                if "error" not in row:
                    done.add(row["question"])
            except Exception:
                continue
    return done


def append_result(row: dict):
    with open(RESULTS_PATH, "a") as f:
        f.write(json.dumps(row) + "\n")


def main():
    data = load_dataset()
    done = already_done_ids()
    print(f"{len(done)} already done, {len(data)} total, {len(data) - len(done)} remaining")

    for i, item in enumerate(data):
        q = item["question"]
        if q in done:
            continue

        try:
            faith = _judge_with_retry(judge_faithfulness, item["answer"], item["contexts"])
            time.sleep(SLEEP_SECONDS)
            prec = _judge_with_retry(judge_context_precision, q, item["contexts"])
            time.sleep(SLEEP_SECONDS)
            recall = _judge_with_retry(judge_context_recall, item["ground_truth"], item["contexts"])
            time.sleep(SLEEP_SECONDS)

            append_result({
                "question": q,
                "faithfulness": faith.get("score"),
                "unsupported_claims": faith.get("unsupported_claims"),
                "context_precision": prec.get("precision"),
                "context_recall": recall.get("score"),
                "missing_claims": recall.get("missing_claims"),
            })
            print(f"[{i+1}/{len(data)}] OK  faith={faith.get('score')} "
                  f"prec={prec.get('precision')} recall={recall.get('score')}")

        except Exception as e:
            # Log and keep going — do NOT let one bad row kill the whole run.
            print(f"[{i+1}/{len(data)}] FAILED: {e}")
            append_result({"question": q, "error": str(e)})
            time.sleep(SLEEP_SECONDS * 2)  # back off harder after a failure


def summarize():
    rows = [json.loads(l) for l in open(RESULTS_PATH) if l.strip()]
    ok = [r for r in rows if "error" not in r]
    def avg(key):
        vals = [r[key] for r in ok if r.get(key) is not None]
        return sum(vals) / len(vals) if vals else None
    print("\n--- SUMMARY ---")
    print(f"Total rows: {len(rows)}  |  Errored: {len(rows) - len(ok)}")
    print(f"Mean faithfulness:       {avg('faithfulness')}")
    print(f"Mean context_precision:  {avg('context_precision')}")
    print(f"Mean context_recall:     {avg('context_recall')}")


if __name__ == "__main__":
    main()
    summarize()