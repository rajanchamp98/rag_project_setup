from app.core.config import settings
from app.llm.embedding_model import get_embedding_model
from app.opensearch.client import get_opensearch_client
from typing import List



def vector_search(
        query:str,
        user_id:str,
        k:int =5
):
    embedding_model=get_embedding_model()

    query_embedding=embedding_model.embed_query(query)

    # print(f"query dimenssion is {len(query_embedding)}")


    client=get_opensearch_client()


    body={
        "size":k,
        "_source":[
            "chunk_id",
            "document_id",
            "user_id",
            "content",
            "metadata",
            "created_at"
        ],
        "query":{
            "knn":{
                "embedding":{
                    "vector":query_embedding,
                    "k":k
                }
            }
        },
        "post_filter":{
            "term":{
                "user_id":user_id
            }
        }
    }

    response=client.search(
        index=settings.OPENSEARCH_INDEX,
        body=body
    )

    results=[]


    for hit in response["hits"]["hits"]:
        results.append({
            "chunk_id": hit["_source"]["chunk_id"],
            "document_id": hit["_source"]["document_id"],
            "user_id": hit["_source"]["user_id"],
            "content": hit["_source"]["content"],
            "metadata": hit["_source"].get("metadata", {}),
            "score": hit["_score"]
        })

    return results



def bm25_search(query:str,user_id:str,k:int=5):
    client=get_opensearch_client()

    body = {
        "size": k,
        "_source": [
            "chunk_id",
            "document_id",
            "user_id",
            "content",
            "metadata",
            "created_at"
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "content": query
                        }
                    }
                ],
                "filter": [
                    {
                        "term": {
                            "user_id": user_id
                        }
                    }
                ]
            }
        }
    }
    response = client.search(
        index=settings.OPENSEARCH_INDEX,
        body=body
    )

    results = []

    for hit in response["hits"]["hits"]:
        results.append({
            "chunk_id": hit["_source"]["chunk_id"],
            "document_id": hit["_source"]["document_id"],
            "user_id": hit["_source"]["user_id"],
            "content": hit["_source"]["content"],
            "metadata": hit["_source"].get("metadata", {}),
            "score": hit["_score"]
        })
    return results



def rrf_fusion(
        vector_results:List[dict],
        bm25_results:List[dict],
        k:int=60,
        top_k:int=10):
    scores={}
    documents={}

    for rank,result in enumerate(vector_results,start=1):
        chunk_id=result["chunk_id"]
        rrf_score=1/(k+rank)
        scores[chunk_id]=scores.get(chunk_id,0)+rrf_score
        documents[chunk_id]=result

    for rank,result in enumerate(bm25_results,start=1):
        chunk_id=result["chunk_id"]
        rrf_score=1/(k+rank)
        scores[chunk_id]=scores.get(chunk_id,0)+rrf_score
        documents[chunk_id]=result

    # sorting to get top result based of rrf fusion score

    ranked_chunk=sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True

    )

    results=[]

    for chunk_id,rrf_score in ranked_chunk:
        result=documents[chunk_id].copy()
        result["rrf_score"] = rrf_score
        results.append(result)

    return results[:top_k]
    



