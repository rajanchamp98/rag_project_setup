from app.rag.retriever import get_retrivers


retriever = get_retrivers()

query = "What is Node.js?"

documents = retriever.invoke(query)

print(f"Retrieved documents: {len(documents)}")

for index, doc in enumerate(documents, start=1):
    print("\n" + "=" * 80)
    print(f"Document {index}")
    print("=" * 80)

    print(doc.page_content)
    print("\nMetadata:")
    print(doc.metadata)