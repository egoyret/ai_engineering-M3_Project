import chromadb
from vectorstore import PERSIST_DIR
from openai import OpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

# Esto es solo para pruebas

load_dotenv() # Carga variable de entorno (api keys, etc)

dominio = "rrhh"

query = "Cuantos dias me corresponden de vacaciones si mi antiguedad es de 4 años ?"

SYSTEM_PROMPT = """
Eres un asistente util
"""
# Capturo el cliente de chroma que se creó en el directorio de persistencia
client = chromadb.PersistentClient(path=str(PERSIST_DIR))

# Capturo la collection del dominio
collection_store = client.get_collection(
        name=dominio)

# Retrieval de los chunks relacionados con la pregunta
results = collection_store.query(
    query_texts=[query],
    n_results=3
)

retrieved_docs = results["documents"][0]
retrieved_ids = results["ids"][0]

# docs = results["documents"][0]
# metas = results["metadatas"][0]
# dists = results["distances"][0]

# Construimos contexto pasandole los chunks recuperados
context_block = ""
for idx, doc in enumerate(retrieved_docs):
    context_block += f"\n[CHUNK {idx + 1} | ID: {retrieved_ids[idx]}]\n{doc}\n"
    # print(f"[DEBUG]\n[CHUNK {idx+1} | ID: {retrieved_ids[idx]}]\n{doc}\n")


# Prompt final
user_prompt = f"""
CONTEXTO:
{context_block}

PREGUNTA DEL USUARIO:
{query}

Recuerda devolver SOLO JSON válido.
"""

# Inicializo el LLM que voy a usar para la RAG query
client_llm = OpenAI()  # Usa la api key de .env
model_llm = "gpt-5-mini"  # Modelo a usar para la RAG query

# Ahora si: hacemos el LLM call con la consulta y el contexto RAG en el system prompt
response = client_llm.chat.completions.create(
    model=model_llm,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ],
    temperature=None
)

raw_output = response.choices[0].message.content

print(raw_output)





