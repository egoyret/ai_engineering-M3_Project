from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.vectorstore import PERSIST_DIR
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

def build_domain_agent(collection_name):

    db = Chroma(
        persist_directory=PERSIST_DIR,
        collection_name=collection_name,

    )

    retriever = db.as_retriever(search_kwargs={"k":4})

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
Responde la pregunta del usuario utilizando solo la información del contexto.

Contexto:
{context}

Pregunta:
{input}
""")

    document_chain = create_stuff_documents_chain(llm, prompt)

    rag_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return rag_chain