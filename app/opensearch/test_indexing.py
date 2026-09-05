from app.core.config import settings
from app.llm.embedding_model import get_embedding_model
from app.opensearch.client import get_opensearch_client


def test_indexing():

    client = get_opensearch_client()
    embedding_model = get_embedding_model()

    content = "OpenSearch is being used for hybrid RAG retrieval."

    embedding = embedding_model.embed_query(content)

    print("Embedding dimension:", len(embedding))

    document = {
        "chunk_id": "test_chunk_001",
        "document_id": "test_document_001",
        "user_id": "test_user_001",
        "content": content,
        "embedding": embedding,
        "metadata": {
            "source": "test.pdf",
            "page": 1
        }
    }

    response = client.index(
        index=settings.OPENSEARCH_INDEX,
        id=document["chunk_id"],
        body=document,
    )

    print("Indexed successfully:")
    print(response)


if __name__ == "__main__":
    test_indexing()