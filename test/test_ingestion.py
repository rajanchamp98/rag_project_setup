from pathlib import Path

from app.rag.pipeline import ingest_document


BASE_DIR = Path(__file__).resolve().parents[1]

print(BASE_DIR)

pdf_path = BASE_DIR / "storage" / "upload" / "nodeJS.pdf"
print(pdf_path.exists())


result = ingest_document(pdf_path)

print(result)