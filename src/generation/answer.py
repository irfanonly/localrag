"""Answer questions from retrieved passages using a local LLM, with citations."""

import re

import ollama

MODEL = "qwen3:4b-instruct-2507-q4_K_M"
NOT_FOUND = "I could not find this in the documents."

SYSTEM_PROMPT = f"""You answer questions using ONLY the numbered context passages provided.
Rules:
- If the passages do not contain the answer, reply exactly: {NOT_FOUND}
- After each claim, cite the passage it came from like [1] or [2].
- Include conditions and exceptions that the passages attach to the answer
  (for example, a number that changes after some years of service).
- State only what a passage says. Do not infer who decides something, or when,
  unless a passage says so.
- Answer in the same language as the question.
- Be concise: 1 to 3 sentences. Do not repeat yourself, and do not list the
  citations again at the end."""


def build_context(hits: list[dict]) -> str:
    blocks = [
        f"[{number}] ({hit['source']}, page {hit['page']})\n{hit['text']}"
        for number, hit in enumerate(hits, start=1)
    ]
    return "\n\n".join(blocks)


def strip_reasoning(text: str) -> str:
    """Remove Qwen3's reasoning. The opening <think> tag belongs to the chat template,
    so the output can contain only the closing tag."""
    if "</think>" in text:
        text = text.rsplit("</think>", 1)[1]
    return text.strip()


def extract_citations(text: str, hits: list[dict]) -> list[dict]:
    """Return the passages the answer cited, ignoring numbers that do not exist."""
    if NOT_FOUND in text:
        return []
    numbers = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
    return [hits[n - 1] for n in sorted(numbers) if 1 <= n <= len(hits)]


def answer(question: str, hits: list[dict], model: str = MODEL) -> tuple[str, list[dict], dict]:
    prompt = f"Context passages:\n\n{build_context(hits)}\n\nQuestion: {question}"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    response = ollama.chat(
        model=model,
        messages=messages,
        # num_ctx: a small context window silently cuts off the passages
        options={"temperature": 0, "num_ctx": 8192},
    )
    text = strip_reasoning(response["message"]["content"])
    stats = {
        "prompt_tokens": response.get("prompt_eval_count"),
        "generated_tokens": response.get("eval_count"),
    }
    return text, extract_citations(text, hits), stats
