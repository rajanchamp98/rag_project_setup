from app.rag.pipeline import ingest_document


result=ingest_document(
    s3_key="documents/6a899a24e77c4bf7878b9aa9/d68745ab-2afd-485e-a44f-8e49c8c7649f/Rajan_kumar_Resume.pdf",
    document_id="d68745ab-2afd-485e-a44f-8e49c8c7649f",
    user_id="6a899a24e77c4bf7878b9aa9"
)

print(result)