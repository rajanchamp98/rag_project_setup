from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document


def chunking(docs:List[Document])->List[Document]:
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,       
    )

    chunks=text_splitter.split_documents(documents=docs)
    return chunks
    