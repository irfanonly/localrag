import ollama

MODEL = "qwen3:4b"

response = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "In one sentence, what is RAG in AI?"}],
)
print(response["message"]["content"])
