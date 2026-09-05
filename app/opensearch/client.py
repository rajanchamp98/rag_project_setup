import boto3

from opensearchpy import OpenSearch,RequestsHttpConnection,AWSV4SignerAuth


from app.core.config import settings


def get_opensearch_client()-> OpenSearch:
    session=boto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    credentials=session.get_credentials()

    if credentials is None:
        raise RuntimeError("Aws credentials not provided")

    auth=AWSV4SignerAuth(
        credentials,
        settings.AWS_REGION,
        "aoss"
    )

    return OpenSearch(
        hosts=[
            {
                "host":settings.OPENSEARCH_ENDPOINT.replace("https://",""),
                "port":443,
            }
        ],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=60,
        max_retries=3,
        retry_on_timeout=True,

    )