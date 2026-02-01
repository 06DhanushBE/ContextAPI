def build_prompt(context: list[str], question: str) -> str:
    context_text = "\n".join(context)

    return f"""
You are a customer support assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say you don't know.

Context:
{context_text}

Question:
{question}

Answer:
""".strip()
