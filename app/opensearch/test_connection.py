from app.opensearch.client import get_opensearch_client
from app.core.config import settings


def test_connection():

    client = get_opensearch_client()

    print("Testing OpenSearch Serverless...")

    exists = client.indices.exists(
        index=settings.OPENSEARCH_INDEX
    )

    print(f"Index exists: {exists}")


if __name__ == "__main__":
    test_connection()