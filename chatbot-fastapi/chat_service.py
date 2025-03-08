from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Any

api_key = "AIzaSyAUOqT3Qhz7aNJPY9ybb5GA17xp9CXmQ6E"

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

# ================================
# Funciones de los agentes
# ================================

def decider_agent(ultimo_mensaje: any) -> str:

    decider_messages = [
        SystemMessage(content="""
Vas a recibir un mensaje de un usuario.
Debes decidir si el usuario esta pidiendo guardar info en la base de cononocimientos o está haciendo una pregunta.
Si pide guardar info, debes responder solo con la palabra "SI", en caso contrario, debes responder con la palabra "NO".
"""),
        HumanMessage(content=ultimo_mensaje["content"])
    ]

    decider_response = decider_model.invoke(decider_messages)

    return decider_response.content


def saver_agent(ultimo_mensaje: any) -> str:

    saver_messages = [
        SystemMessage(content="""
Vas a recibir un mensaje de un usuario.
Debes guardar la info en la base de cononocimientos.
"""),
        HumanMessage(content=ultimo_mensaje["content"])
    ]

    saver_response = saver_model.invoke(saver_messages)

    return saver_response.content


def qa_agent(ultimo_mensaje: any) -> str:

    qa_messages = [
        SystemMessage(content="""
Vas a recibir un mensaje de un usuario.
Debes responder la pregunta del usuario basada en la infomracion extraida de la base de conocimientos.
"""),
        HumanMessage(content=ultimo_mensaje["content"])
    ]

    qa_response = qa_model.invoke(qa_messages)

    return qa_response.content


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

    qa_response = qa_agent(ultimo_mensaje)

    return qa_response