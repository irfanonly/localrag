import sys

from retrieval.store import get_collection, search

query = " ".join(sys.argv[1:])
for hit in search(get_collection(), query):
    print(f"[{hit['score']:.2f}] {hit['source']} p.{hit['page']} ({hit['language']})")
    print(hit["text"][:300].replace("\n", " "), "\n")
