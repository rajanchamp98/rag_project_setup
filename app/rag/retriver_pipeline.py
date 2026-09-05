from app.rag.retrieve import vector_search,bm25_search,rrf_fusion
from app.rag.reranker import reranker
from typing import List

def retrieve_documents(query:str,user_id:str)->List[dict]:

    #vector serach

    result_vector_search=vector_search(query=query,user_id=user_id,k=10)

    #bm25 serach

    result_bm25_search=bm25_search(query,user_id,10)

    result_rrf_fusion=rrf_fusion(vector_results=result_vector_search,
                                 bm25_results=result_bm25_search,
                                 top_k=20,
                                )

    #reranking:

    result_reranking=reranker(
        query=query,
        documents=result_rrf_fusion,
        top_k=5
    )

    return result_reranking