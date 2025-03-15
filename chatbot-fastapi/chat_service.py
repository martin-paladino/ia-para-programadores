from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from typing import Any
import uuid

api_key = "AIzaSyAUOqT3Qhz7aNJPY9ybb5GA17xp9CXmQ6E"

# ================================
# Configuración de los modelos
# ================================

# Inicializa los modelos de lenguaje para cada agente.
# Cada agente utiliza un modelo distinto con configuraciones específicas.

# Modelo para el agente que decide si se debe guardar info o no.
decider_model = init_chat_model(
    "gemini-2.0-flash-lite",
    model_provider="google_genai",
    temperature=0.1,
    api_key=api_key
)

# Modelo para el agente que guarda info en la base de conocimientos.
saver_model = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.1,
    api_key=api_key
)

# Modelo para el agente que responde preguntas.
qa_model = init_chat_model(
    "gemini-1.5-pro",
    model_provider="google_genai",
    temperature=0.7,
    api_key=api_key
)

# ================================
# Configuración de la base de datos vectorial
# ================================
vector_database = None

def get_vector_databse():
    global vector_database
    if vector_database is None:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        vector_database = InMemoryVectorStore(embeddings)
    return vector_database


# ================================
# Estado o memoria de trabajo de los agentes
# ================================

# Siguiendo el modelo recomendado en la documentación de LangGraph:
# https://langchain-ai.github.io/langgraph/tutorials/introduction/#part-1-build-a-basic-chatbot
class AgentsState(BaseModel):
    """
    Define el esquema o memoria de trabajo para el grafo de agentes.
    
    Atributos:
        query: El mensaje o consulta del usuario.
        decided_to_save: Indica si el usuario quiere guardar información.
        chat_history: Historial de la conversación.
    """
    query: dict[str, Any]
    decided_to_save: bool
    chat_history: list[dict[str, Any]]
    context: list[Document]


# ================================
# Funciones de los agentes (nodos del grafo)
# ================================
def decider_agent(state: AgentsState):
    """
    Determina si el usuario quiere guardar información o hacer una consulta.
    
    Este agente analiza el mensaje del usuario y decide la intención:
    - Guardar información en la base de conocimientos
    - Realizar una consulta para obtener información

    Args:
        state: Estado actual del grafo, que incluye el mensaje del usuario y el historial de la conversación.
        
    Returns:
        El estado actualizado con la decisión del agente.
    """
    print("entro al decider agent")
    decider_messages = [
        SystemMessage(content="""
            Vas a recibir un mensaje de un usuario.
            Debes decidir si el usuario esta pidiendo guardar info en la base de cononocimientos o está haciendo una pregunta.
            Si pide guardar info, debes responder solo con la palabra "SI", en caso contrario, debes responder con la palabra "NO".
        """),
        HumanMessage(content=state.query["content"])
    ]

    decider_response = decider_model.invoke(decider_messages)

    # Actualiza el estado con la decisión del agente
    state.decided_to_save = True if decider_response.content == "SI" else False
    print("respuesta del decider agent: ", decider_response.content)
    return state


def saver_agent(state: AgentsState):
    """
    Guarda información en la base de conocimientos y le informa al usuario que se ha guardado.
    
    Este agente toma el texto proporcionado por el usuario y lo almacena en la base de conocimientos.

    Args:
        state: Estado actual del grafo, que incluye el mensaje del usuario y el historial de la conversación.
        
    Returns:
        El estado actualizado con la respuesta del agente.
    """
    print("entro al saver agent")
    
    # Utilizamos la base de datos vectorial para guardar la información
    vector_database = get_vector_databse()
    document = Document(
        page_content=state.query["content"],
        metadata={"id": str(uuid.uuid4())},
    )
    print("documento a guardar: ", document)
    documents = [document]
    vector_database.add_documents(documents=documents)

    saver_messages = [
        SystemMessage(content="""
            Vas a recibir un mensaje de un usuario.
            Debes guardar la info en la base de cononocimientos.
        """),
        HumanMessage(content=state.query["content"])
    ]
    saver_response = saver_model.invoke(saver_messages)
    print("respuesta del saver agent: ", saver_response.content)

    # Actualiza el historial de la conversación con la respuesta del agente
    state.chat_history.append({
        "role": "assistant",
        "content": saver_response.content
    })

    return state


def qa_agent(state: AgentsState):
    """
    Responde a consultas usando RAG (Retrieval Augmented Generation).
    
    Este agente busca información relevante en la base de conocimientos,
    recupera los documentos más similares y genera una respuesta basada en ellos.

    Args:
        state: Estado actual del grafo, que incluye el mensaje del usuario y el historial de la conversación.
        
    Returns:
        El estado actualizado con la respuesta del agente.
    """
    print("entro al qa agent")
    vector_database = get_vector_databse()
    docs = vector_database.similarity_search(state.query["content"], k=3)
    state.context = docs
    print("docs: ", docs)

    qa_messages = [
        SystemMessage(content="""
            Vas a recibir un mensaje de un usuario.
            Debes responder la pregunta del usuario basada en la infomracion extraida de la base de conocimientos.
        """),
        HumanMessage(content=state.query["content"]),
        HumanMessage(content=f"Esta es la informacion relevante para responder: {state.context}")
    ]

    qa_response = qa_model.invoke(qa_messages)

    # Actualiza el historial de la conversación con la respuesta del agente
    state.chat_history.append({
        "role": "assistant",
        "content": qa_response.content
    })

    print("respuesta del qa agent: ", qa_response.content)
    return state


# ===================================================================
# GRAFO DE AGENTES
# ===================================================================
def create_agents_graph():
    """
    Crea el grafo de agentes para el chatbot.
    """

    # Inicializar el grafo con el esquema de estado o memoria de trabajo
    # definido previamente
    graph = StateGraph(AgentsState)

    # Agregar los nodos (agentes) del grafo
    graph.add_node("decider", decider_agent)
    graph.add_node("saver", saver_agent)
    graph.add_node("qa", qa_agent)

    # Función para decidir qué agente llamará el decider agent
    def decide_next_agent(state: AgentsState) -> str:
        # Si el decider agent respondió "SI" y actualizó el estado de decided_to_save a True, 
        # llama al saver agent. En caso contrario, llama al qa agent.
        if state.decided_to_save == True:
            return "saver"
        else:
            return "qa"

    # Definir el nodo inicial del grafo
    graph.add_edge(START, "decider")

    # Definir las aristas/flechas (edges) del grafo
    graph.add_conditional_edges(
        "decider",
        decide_next_agent
    )

    # Definir los nodos finales del grafo
    graph.add_edge("saver", END)
    graph.add_edge("qa", END)

    # Compilar el grafo para que se pueda ejecutar
    compiled_graph = graph.compile()

    return compiled_graph

# Se crea el grafo de agentes
AGENTS_GRAPH = create_agents_graph()


# ================================
# Procesamiento de mensajes
# ================================
def process_message(data: dict) -> dict:
    """
    Procesa una solicitud del usuario utilizando el grafo de agentes.
    
    Esta función es el punto de entrada principal para el chatbot:
    1. Extrae el mensaje del usuario y el historial de chat
    2. Ejecuta el grafo de agentes para determinar la acción y generar la respuesta
    3. Devuelve la respuesta con el historial actualizado
    
    Args:
        data (dict): Datos de la solicitud con la lista de mensajes
        
    Returns:
        dict: Respuesta con los mensajes actualizados y metadatos
    """

    # Extrae el último mensaje del historial de mensajes
    last_message = data.get("messages", [])[-1]

    # Inicializar el estado o memoria de trabajo
    agents_state = AgentsState(
        query=last_message,
        decided_to_save=False,
        chat_history=[],
        context=[]
    )

    # Ejecutar el grafo con el estado inicial
    updated_state = AGENTS_GRAPH.invoke(agents_state)

    return updated_state
