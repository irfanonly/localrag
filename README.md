# LocalRAG

> Private, offline-capable Q&A over your documents, with source citations. Built for Arabic and English.

![demo](docs/demo.gif) <!-- add later -->



## The problem
LLMs do not know your private documents and may hallucinate. Ctrl+F only matches exact words.
LocalRAG finds the relevant passages by meaning, answers only from them, and shows where each answer came from.

## Sample data
Public Saudi labor law documents (Arabic and English), downloaded from official
sources. See `data/samples/sources.csv` for origins and versions.
English texts are translations for guidance; the Arabic text governs.

## Features (planned)
- [ ] PDF ingestion with page-level citations
- [ ] Arabic and English support
- [ ] Fully local mode (Ollama), optional cloud LLM via config
- [ ] Hybrid search (BM25 + vectors) with reranking
- [ ] Evaluation suite with published results
- [ ] FastAPI backend and web UI
- [ ] Docker one-command setup

## Architecture
_Diagram coming in Phase 6._

## Quick start
_Coming soon._

## Evaluation results
| Setting | Hit rate@5 | Answer quality |
|---|---|---|
| Baseline | TBD | TBD |

## Limitations
_To be filled in as the project develops._

## Lessons learned
_To be filled in as the project develops._

## License
MIT
