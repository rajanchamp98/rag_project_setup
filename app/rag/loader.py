from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from typing import List

def doc_loader(path:Path)->List[Document]:
    loader=PyPDFLoader(file_path=str(path),)

    document=loader.load()

    return document
