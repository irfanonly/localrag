import argparse
import re
import time
from pathlib import Path

from generation.answer import answer
from retrieval.store import get_collection, search

ARABIC = re.compile(r"[\u0600-\u06FF]")

parser = argparse.ArgumentParser()
parser.add_argument("question")
parser.add_argument("--k", type=int, default=3, help="passages to retrieve")
parser.add_argument("--any-language", action="store_true", help="search both languages")
args = parser.parse_args()

# By default, search only the documents in the language of the question
language = None if args.any_language else ("ar" if ARABIC.search(args.question) else "en")
hits = search(get_collection(), args.question, k=args.k, language=language)

start = time.perf_counter()
text, sources, stats = answer(args.question, hits)
elapsed = time.perf_counter() - start

lines = [text, "", "Sources:"]
lines += [f"- {hit['source']}, page {hit['page']}" for hit in sources] or ["- (none cited)"]
lines += [
    "",
    f"({len(hits)} passages, {stats['prompt_tokens']} prompt tokens, "
    f"{stats['generated_tokens']} generated tokens, {elapsed:.0f}s)",
]
output = "\n".join(lines)

print(output)
Path("scratch").mkdir(exist_ok=True)
Path("scratch/last_answer.txt").write_text(output, encoding="utf-8")  # readable in VS Code
