from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

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
# Procesamiento de mensajes
# ================================
def process_message(messages):
    """
    Procesa un mensaje y devuelve una respuesta
    
    Args:
        message: El mensaje del usuario
        
    Returns:
        La respuesta al mensaje
    """

    ultimo_mensaje = messages[-1]

    decider_messages = [
        SystemMessage(content="""
Vas a recibir un mensaje de un usuario.
Debes decidir si el usuario esta pidiendo guardar info en la base de cononocimientos o está haciendo una pregunta.
Si pide guardar info, debes responder solo con la palabra "SI", en caso contrario, debes responder con la palabra "NO".
"""),
        HumanMessage(content=ultimo_mensaje)
    ]

    decider_response = decider_model.invoke(decider_messages)
