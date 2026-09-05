
from typing import List
from app.core.config import settings
from sentence_transformers import CrossEncoder


reranker_model=CrossEncoder(settings.RERANK_MODEL_NAME)



def reranker(
        query:str,
        documents:List[dict],
        top_k:int=5
             )->List[dict]:

             if not documents:
                     return []

             pairs=[(query,document["content"]) for document in documents]

             scores=reranker_model.predict(pairs)

             scored_document=[]

             for document,score in zip(documents,scores):
                     result=document.copy()
                     result["rank_score"]=float(score)
                     scored_document.append(result)

             scored_document.sort(
                     key=lambda x:x["rank_score"],
                     reverse=True
             )

             return scored_document[:top_k]