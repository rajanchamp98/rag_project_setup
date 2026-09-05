from app.rag.retrieve import get_retrivers

def retrive_for_chat(question:str,history:list):
    retriver=get_retrivers()

    document=retriver.invoke(question)

    