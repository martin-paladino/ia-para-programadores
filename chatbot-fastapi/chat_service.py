from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Any, TypedDict, Dict, List
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel

api_key = "TU_API_KEY_AQUI"

# ================================
# Configuración de los modelos
# ================================
decider_model = init_chat_model(
    "gemini-2.0-flash-lite",
    model_provider="google_genai",
    temperature=0.1,
    api_key=api_key
)
saver_model = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.1,
    api_key=api_key
)
qa_model = init_chat_model(
    "gemini-1.5-pro",
    model_provider="google_genai",
    temperature=0.7,
    api_key=api_key
)

# Definir el estado usando una clase Pydantic en lugar de TypedDict
class AgentsState(BaseModel):
    query: Dict[str, Any]
    decided_to_save: bool = False  # Valor predeterminado
    chat_history: List[Dict[str, Any]] = []

# ================================
# Funciones de los agentes
# ================================

def decider_agent(state: AgentsState):

    decider_messages = [
        SystemMessage(content="""
Vas a recibir un mensaje de un usuario.
Debes decidir si el usuario esta pidiendo guardar info en la base de cononocimientos o está haciendo una pregunta.
Si pide guardar info, debes responder solo con la palabra "SI", en caso contrario, debes responder con la palabra "NO".
"""),
        HumanMessage(content=state.query["content"])
    ]

    decider_response = decider_model.invoke(decider_messages)

    state.decided_to_save = True if decider_response.content == "SI" else False

    return state

def saver_agent(state: AgentsState):

    saver_messages = [
        SystemMessage(content="""
Vas a recibir un mensaje de un usuario.
Debes guardar la info en la base de cononocimientos.
"""),
        HumanMessage(content=state.query["content"])
    ]

    saver_response = saver_model.invoke(saver_messages)

    state.chat_history.append({
        "role": "assistant",
        "content": saver_response.content
    })

    return state

def qa_agent(state: AgentsState):

    qa_messages = [
        SystemMessage(content="""
Vas a recibir un mensaje de un usuario.
Debes responder la pregunta del usuario basada en la infomracion extraida de la base de conocimientos.
"""),
        HumanMessage(content=state.query["content"])
    ]

    qa_response = qa_model.invoke(qa_messages)

    state.chat_history.append({
        "role": "assistant",
        "content": qa_response.content
    })

    return state


# ================================
# Procesamiento de mensajes
# ================================
def process_message(data: Any) -> str:
    """
    Procesa un mensaje y devuelve una respuesta
    
    Args:
        data: Los datos recibidos (cualquier tipo)
        
    Returns:
        La respuesta al mensaje
    """

    ultimo_mensaje = data.get("messages", [])[-1]

    agents_state = AgentsState(
        query=ultimo_mensaje,
        decided_to_save=False,
        chat_history=[]
    )

    # Definir el grafo con el esquema de estado apropiado
    graph = StateGraph(AgentsState)

    graph.add_node("decider", decider_agent)
    graph.add_node("saver", saver_agent)
    graph.add_node("qa", qa_agent)


    def decidir_que_agente_llamar(state: AgentsState) -> str:
        if state.decided_to_save == True:
            return "saver"
        else:
            return "qa"

    graph.add_edge(START, "decider")
    graph.add_conditional_edges(
        "decider",
        decidir_que_agente_llamar
    )
    graph.add_edge("saver", END)
    graph.add_edge("qa", END)

    compiled_graph = graph.compile()

    response = compiled_graph.invoke(agents_state)

    return response
