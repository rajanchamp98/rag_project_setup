from app.core.config import settings
from app.llm.embedding_model import get_embedding_model
from datetime import datetime,timezone
from app.opensearch.client import get_opensearch_client
from opensearchpy.helpers import bulk



def index_chunk(
        chunks,
        document_id:str,
        user_id:str
)->None:
    emdedding_model=get_embedding_model()

    texts=[chunk.page_content for chunk in chunks]

    print("generating embedding for texts",len(texts))

    embeddings=emdedding_model.embed_documents(texts)

    actions=[]

    for index,(chunk,embedding) in enumerate(zip(chunks,embeddings)):
        chunk_id=f"{document_id}_{index}"
        actions.append({
            "_index":settings.OPENSEARCH_INDEX,
            "_id":chunk_id,
            "_source":{
                "chunk_id":chunk_id,
                "document_id":document_id,
                "user_id":user_id,
                "content":chunk.page_content,
                "embedding":embedding,
                "metadata":chunk.metadata,
                "created_at":datetime.now(timezone.utc)
            }
        })


        if(not actions):
            print("No chunks to index")
            return

        client=get_opensearch_client()

        success,failed=bulk(
            client=client,
            actions=actions,
            chunk_size=500,
            raise_on_error=False
            
        )

    print(f"Indexed Chunks : {success}")
    print(f" Failed chunks :{len(failed)} ")









