from app.opensearch.client import get_opensearch_client
from app.core.config import settings

client=get_opensearch_client()

response = client.get(
    index=settings.OPENSEARCH_INDEX,
    id="test_chunk_001"
)

print(response)