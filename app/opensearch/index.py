from app.opensearch.client import get_opensearch_client
from app.core.config import settings


def create_document_index():
    client=get_opensearch_client()
    index_name=settings.OPENSEARCH_INDEX

    if client.indices.exists(index=index_name):
        print("Index already exist")
        return
    
    index_body = {
        "settings": {
            "index": {
                "knn": True
            }
        },
        "mappings": {
            "properties": {
                "chunk_id": {
                    "type": "keyword"
                },

                "document_id": {
                    "type": "keyword"
                },

                "user_id": {
                    "type": "keyword"
                },

                "content": {
                    "type": "text"
                },

                "embedding": {
                    "type": "knn_vector",
                    "dimension": 1024
                },

                "metadata": {
                    "type": "object"
                },

                "created_at": {
                    "type": "date"
                }
            }
        }
    }

    response=client.indices.create(
        index=index_name,
        body=index_body
    )

    print(response)

create_document_index()