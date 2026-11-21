from retrieval.embedder import embed
from retrieval.store import get_collection

NEEDLE = "التاسعة بعد المائة"  # heading of Article 109 in the Arabic Labor Law
QUERY = "كم مدة الإجازة السنوية للعامل؟"

collection = get_collection()

# 1. Does a chunk containing the Article 109 heading exist at all?
stored = collection.get(where={"source": "labor_law_ar.pdf"}, include=["documents"])
holders = [i for i, doc in zip(stored["ids"], stored["documents"], strict=True) if NEEDLE in doc]
print("Chunks containing the heading:", holders or "NONE")

# 2. If it exists, where does it rank for the Arabic question?
result = collection.query(query_embeddings=embed([QUERY]), n_results=50, where={"language": "ar"})
for rank, chunk_id in enumerate(result["ids"][0], start=1):
    if chunk_id in holders:
        print(f"Rank for the Arabic question: {rank} ({chunk_id})")
        break
else:
    print("Not in the top 50 results")
