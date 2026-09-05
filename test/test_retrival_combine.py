from app.rag.retriver_pipeline import retrieve_documents

query = "what is Rajan's hobby"
user_id = "6a899a24e77c4bf7878b9aa9"

reranked_results = retrieve_documents(query=query,user_id=user_id)


print("\n========== RERANKED RESULTS ==========")

for rank, result in enumerate(reranked_results, start=1):
    print(
        f"{rank}. "
        f"{result['chunk_id']} | "
        f"Rerank: {result['rank_score']:.6f}"
    )

    print(result["content"])
    print("-" * 80)