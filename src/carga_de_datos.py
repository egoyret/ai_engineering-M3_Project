import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import logger, PROJECT_ROOT

# Get the project root directory (parent of src directory)
# PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE_FINANZAS = PROJECT_ROOT / "data" / "finanzas.txt"
DATA_FILE_RRHH = PROJECT_ROOT / "data" / "recursos_humanos.txt"
DATA_FILE_IT = PROJECT_ROOT / "data" / "soporte_it.txt"
DATA_FILE_LEGAL = PROJECT_ROOT / "data" / "legal.txt"
DATA_FILE_EVALUADOR = PROJECT_ROOT / "data" / "evaluador.txt"

CHUNK_SIZE = 350
CHUNK_OVERLAP = 80

def leer_archivos(data_file):
    textos = []
    with open(data_file, "r", encoding="utf-8") as f:
        textos.append(f.read())

    return "\n".join(textos)

def parsear_politicas(texto):

    politicas = []

    bloques = re.split(r"\n\s*TEMA:", texto)
    for bloque in bloques:
        bloque = bloque.strip()
        if not bloque:
            continue
        bloque = "TEMA:" + bloque if not bloque.startswith("TEMA:") else bloque
        tema_match = re.search(r"TEMA:\s*(.*)", bloque)
        desc_match = re.search(r"DESCRIPCION:\s*([\s\S]*)", bloque)
        if tema_match and desc_match:
            tema = tema_match.group(1).strip()
            descripcion = desc_match.group(1).strip()
            politicas.append({
                "tema": tema,
                "descripcion": descripcion
            })

    return politicas

def crear_splitter():

    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

def generar_chunks(politicas, dominio):

    splitter = crear_splitter()
    chunks = []

    chunk_id = 1

    for doc_id, politica in enumerate(politicas):

        partes = splitter.split_text(politica["descripcion"])

        for i, chunk in enumerate(partes):

            chunks.append({
                "chunk_id": chunk_id,
                "tema": politica["tema"],
                "chunk_index": i,
                "texto": chunk,
                "metadata": {
                    "categoria": politica["tema"],
                    "documento_id": str(doc_id),
                    "dominio": dominio
                }
            })

            chunk_id += 1

    return chunks

def carga_base_de_conocimientos(dominio):
    match dominio.lower():
        case "finanzas":
            file = DATA_FILE_FINANZAS
        case "rrhh":
            file = DATA_FILE_RRHH
        case "soporte_it":
            file = DATA_FILE_IT
        case "legal":
            file = DATA_FILE_LEGAL
        case _:
            file = None
    texto = leer_archivos(file)
    politicas = parsear_politicas(texto)
    chunks = generar_chunks(politicas, dominio)
    # logger.info(f"Base {dominio} cargada con {len(chunks)} chunks")
    return chunks

def cargar_dataset_evaluador():
    resultados = []
    filepath = DATA_FILE_EVALUADOR

    with open(filepath, "r", encoding="utf-8") as f:
        texto = f.read()

    pattern = r"PREGUNTA:\s*(.*?)\s*DATASET_CORRECTO:\s*(.*?)\s*(?:\n|$)"

    matches = re.findall(pattern, texto, re.DOTALL)

    for pregunta, dataset in matches:
        resultados.append({
            "pregunta": pregunta.strip(),
            "dataset_correcto": dataset.strip()
        })

    return resultados


def main():

    print("Leyendo archivos de texto...")

    texto = leer_archivos(DATA_FILE_FINANZAS)
    print(f"Archivo de texto leido: {len(texto)} caracteres")

    print("Parseando políticas...")

    politicas = parsear_politicas(texto)

    print(f"Políticas encontradas: {len(politicas)}")

    print("Generando chunks...")

    chunks = generar_chunks(politicas, "finanzas")

    print(f"Chunks generados: {len(chunks)}")

if __name__ == "__main__":
    # main()
    dataset = cargar_dataset_evaluador()
    print(dataset[0])
    print(len(dataset))
