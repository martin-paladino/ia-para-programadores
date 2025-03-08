# Chatbot Inteligente con FastAPI, Langchain y LangGraph

Este proyecto forma parte del curso **"IA para programadores"** y demuestra la implementación de un chatbot inteligente que utiliza agentes para procesar mensajes de usuarios de manera orquestada.

## Descripción

El chatbot implementa un sistema de decisión inteligente que:
1. Recibe mensajes del usuario
2. Determina si el usuario quiere guardar información o está haciendo una pregunta
3. Según la decisión, deriva el mensaje al agente adecuado:
   - **Saver Agent**: Procesa y guarda la información proporcionada
   - **QA Agent**: Responde preguntas basándose en la información previamente guardada

La arquitectura utiliza LangGraph para definir un flujo de trabajo entre diferentes modelos de IA, donde cada uno tiene una responsabilidad específica dentro del sistema.

## Requisitos

- Python 3.9+
- API Key de Google Gemini

## Dependencias principales

- FastAPI: Framework web para la API REST
- Uvicorn: Servidor ASGI para FastAPI
- Pydantic: Validación de datos
- LangChain: Framework para trabajar con modelos de lenguaje
- LangGraph: Orquestación de flujos de trabajo con LLMs

## Instalación

1. Clonar el repositorio:
```bash
git clone <repositorio>
cd chatbot-fastapi
```

2. Crear y activar un entorno virtual:

   **Para todos los sistemas:**
   ```bash
   python -m venv venv
   ```

   **Activar el entorno virtual:**
   
   - **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   
   - **Windows (PowerShell):**
   ```powershell
   venv\Scripts\Activate.ps1
   ```
   
   - **Windows (Command Prompt):**
   ```cmd
   venv\Scripts\activate.bat
   ```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la API key de Google Gemini:
   - Edita el archivo `chat_service.py`
   - Reemplaza `"TU_API_KEY_AQUI"` con tu API key de Google Gemini

## Ejecución

Para iniciar el servidor:

```bash
uvicorn main:app --reload --port 8001
```

El servidor estará disponible en http://localhost:8001

## Uso del API

### Endpoint de chat

```
POST /chat
```

Ejemplo de solicitud:

```bash
curl -X 'POST' \
  'http://localhost:8001/chat' \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
      {
        "role": "user", 
        "content": "Guarda que la capital de Francia es París"
      }
    ]
  }'
```

Ejemplo de respuesta:
```json
{
  "response": "He guardado la información: la capital de Francia es París."
}
```

## Arquitectura del sistema

El proyecto utiliza una arquitectura basada en agentes con LangGraph:

1. **Decider Agent**: Analiza el mensaje del usuario y determina si es una solicitud para guardar información o una pregunta.
2. **Saver Agent**: Se activa cuando el usuario quiere guardar información en la base de conocimientos.
3. **QA Agent**: Se activa cuando el usuario hace una pregunta, consultando la base de conocimientos para proporcionar una respuesta.

El flujo de trabajo se define mediante un grafo dirigido que conecta estos agentes según la decisión tomada por el Decider Agent.

### Estructura de archivos

- `main.py`: Define los endpoints de FastAPI
- `chat_service.py`: Contiene la lógica de los agentes y el grafo de flujo de trabajo
- `requirements.txt`: Lista de dependencias


## Contexto educativo

Este proyecto es parte del curso **"IA para programadores"**, diseñado para enseñar cómo integrar modelos de lenguaje en aplicaciones prácticas mediante el uso de LangChain y LangGraph dentro de un entorno web con FastAPI. 