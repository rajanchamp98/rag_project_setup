from app.rag.retrieve import bm25_search


results = bm25_serach(
    query="What AI projects has Rajan worked on?",
    user_id="6a899a24e77c4bf7878b9aa9",
    k=5
)

print("\n========== RESULTS ==========\n")

for index, result in enumerate(results, start=1):
    print(f"Result {index}")
    print(f"Chunk ID: {result['chunk_id']}")
    print(f"Score: {result['score']}")
    print(f"Content:\n{result['content']}")
    print("-" * 80)