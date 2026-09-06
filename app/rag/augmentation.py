from typing import List


def build_context(documents:List[dict])->str:
    context_part=[]

    for index,documnet in enumerate(documents,start=1):
        context_part.append(
            f"[context {index}]\n"
            f"{documnet["content"]}"
            )

    return "\n\n".join(context_part)


def build_prompt(
    query: str,
    context: str,
    history:str
) -> str:

    return f"""
You are a helpful AI assistant.

Answer the user's question using only the provided context.

Rules:
- Use the provided context as the primary source.
- Do not invent or assume information.
- If the answer is not present in the context, say:
  "I don't have enough information in the provided documents."
- Answer directly and concisely.
- Include relevant details from the context when useful.
- Do not mention that you are using a context or RAG system.

Conversation History:
{history}

Context:
{context}

User Question:
{query}
""".strip()


def built_history(history):
    if len(history)==0:
        return []
    history_store=[]

    for message in history:
        role=message["role"]
        content=message["content"]
        history_store.append(
            f"{role.capitalize()}:{content}"
        )

    return "\n".join(history_store)



