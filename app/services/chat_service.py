from app.rag.retrieve import get_retrivers
from app.llm.chat_model import get_chat_model



def process_chat(message:str)->str:
    retriver=get_retrivers()

    document=retriver.invoke(message)

    context="\n\n".join(
        doc.page_content for doc in document
    )

    llm=get_chat_model()

    prompt = f"""
    You are a helpful RAG assistant.

    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {message}

    Answer:
    """

    response=llm.invoke(prompt)

    return response.content
    
    

