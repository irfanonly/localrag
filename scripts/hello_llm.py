import time

import ollama

MODEL = "qwen3:4b"

start = time.perf_counter()
response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "In one sentence, what is RAG in AI?"}],
    think=False,
)
print(response["message"]["content"])
print(f"\nTook {time.perf_counter() - start:.1f}s")