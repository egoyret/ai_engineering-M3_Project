# ai_engineering-M3_Project
Routing inteligente de soporte al cliente

## Consigna
Desarrolla un sistema multiagente en el que un Agente Orquestador clasifique la intención de la consulta del usuario (por ejemplo, RR. HH. o Tecnología). Esta clasificación activa un enrutamiento condicional que delega la tarea de recuperación al Agente RAG especializado correcto, para generar una respuesta contextualmente fundamentada. Todo el flujo dinámico debe implementarse con LangChain y quedar trazado completamente con Langfuse.

## Pasos

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/egoyret/ai_engineering-M3_Project.git
   ```

2. Creá y activá un entorno virtual (desde el root del proyecto):

   * **venv** (Linux/macOS/Windows PowerShell):

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate    # Unix/macOS
 
     ```
3. Instalá las dependencias:

   ```bash
   pip install -r requirements.txt
   ```
4. Agrega las API key de OpenAI y LangFuse en tu .env file (template de .env en .env.example en el root):
    ```bash
   OPENAI_API_KEY=<your api key>
      ```
   
## Estructura del proyecto

```
ai_engineering-M3_Project/
├── data/
│   ├── finanzas.txt  # Base de conocimeinto de Finanzas
│   ├── legal.txt  # Base de conocimeinto de Legal
│   ├── recursos_humanos.txt  # Base de conocimeinto de RRHH
│   ├── soporte.txt  # Base de conocimeinto de Soporte IT
│   ├── preguntas.txt  # Consultas ejemplo
│   ├── evaluador.txt  # Preguntas con evaluacion para pruebas
│
├── chroma_db/         # folder para el vector store   
├── src/
│   ├── main.ipynb                               # Notebook de ejecución
│   ├── carga_de_datos.py                        # Carga dataos y genera los chunks
│   ├── utils.py                                 # Utilidades
│   ├── vectorstore.py                           # Generacion y almacenamiento embeddings
│   ├── agentes/                                 # Construccion de agentes
```

## Ejecución:

Ejecutar el notebook main.ipynb para ver el flujo de ejecucion del chatbot.


## Tecnologias utilizadas:

- Las bases de conocimiento son archivos de texto que se convierten a json y luego se chunkean.
- Se utiliza Chroma para almacenar el vector store con los embeddings generados de las bases de conocimientos. Una coleccion por cada dominio d einformación.
- Los agentes para cada dominio se construyen dinámicamente.
- Se utiliza LangChain para los RAG de los agentes
- Se utiliza LangGraph para el arbol de nodos
- Se utiliza Langfuse para evaluar la calidad de las respuestas generadas por el chatbot.
- 

**Estrategia de chunking:**

En base al tamaño d elos textos de las bases de conocimiento se decidió usar chunks de 350 con solapamiento de 80 caracteres.

**Modelo de LLM:**

Para el RAG usamos un modelo de OpenAI al que le pasamos en el contexto los chunks previamente seleccionados por la 'collections' de Chroma.


