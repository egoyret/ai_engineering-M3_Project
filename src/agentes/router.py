from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def route_question(question):

    prompt = f"""
Clasifica la siguiente pregunta en una de estas categorías:

HR
IT
LEGAL
FINANCE

Pregunta:
{question}

Responde solo con la categoría.
"""

    response = llm.invoke(prompt)

    return response.content.strip()
