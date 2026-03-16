import os
import shutil

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from src.carga_de_datos import carga_base_de_conocimientos
from utils import PROJECT_ROOT, logger

INPUT = "politicas_chunks.json"
PERSIST_DIR = PROJECT_ROOT / "chroma_db"
COLLECTION_NAME = "politicas"


def initialize_chroma(model):
    # Eliminar directorio de base de datos antiguo para evitar problemas de datos antiguos
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)
    embedding_function = OpenAIEmbeddingFunction(model_name=model)
    client = chromadb.PersistentClient(path=str(PERSIST_DIR))
    return client, embedding_function

def create_collection(client, embedding_function, dominio):

    # Creo el dataset para los embeddings que se van a generar con el modelo definido.
    try: # Primero borro el dataset si existe
        client.delete_collection(name=dominio)
    except Exception:
        pass

    collection = client.create_collection(
        name=dominio,
        embedding_function=embedding_function)

    # logger.info(f"Collection {dominio} created")
    return collection


def genera_y_almacena_embeddings(chunks, collection):
    ids = []
    metadatas = []
    documents = []

    for chunk in chunks:
        metadata = chunk["metadata"]
        ids.append("Id_" + str(chunk["chunk_id"]))
        metadatas.append({"category": metadata["categoria"]})
        documents.append(chunk["texto"])

    # Add all documents in batch for better persistence
    collection.add(
        ids=ids,
        metadatas=metadatas,
        documents=documents
    )

def listar_collections():
    client = chromadb.PersistentClient(path=str(PERSIST_DIR))
    return client.list_collections()


def main():
    from dotenv import load_dotenv
    load_dotenv()
    dominio = "finanzas"

    collection = initialize_chroma(dominio)
    chunks = carga_base_de_conocimientos(dominio)
    genera_y_almacena_embeddings(chunks, collection)
    logger.info(
        f"Cargado {len(chunks)} chunks para el dominio {dominio}"
    )
    print("vector db cargada")


if __name__ == "__main__":
    main()
