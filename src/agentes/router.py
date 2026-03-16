from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


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

Responde solo con la categoría. Si no corresponde a ninguna de las categorias responde con NA
"""

    response = llm.invoke(prompt)

    return response.content.strip()

def main():

    question = "Cual es el actor principal de la pelicula back to the future ?"
    resp = route_question(question)
    print(resp)


if __name__ == "__main__":
    main()