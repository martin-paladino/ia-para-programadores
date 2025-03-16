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

## Características

- **Interfaz Web Moderna**: Interfaz de usuario intuitiva y responsive para interactuar con el chatbot
- **Sistema de Agentes Inteligentes**: Utiliza múltiples modelos de Google Gemini para diferentes tareas
- **Almacenamiento Vectorial**: Guarda información en una base de datos vectorial para búsquedas semánticas
- **Orquestación con LangGraph**: Flujo de trabajo flexible y estructurado entre agentes

## Requisitos

- Python 3.9+
- API Key de Google Gemini

## Dependencias principales

- FastAPI: Framework web para la API REST
- Uvicorn: Servidor ASGI para FastAPI
- Pydantic: Validación de datos
- LangChain: Framework para trabajar con modelos de lenguaje
- LangGraph: Orquestación de flujos de trabajo con LLMs
- LangChain HuggingFace: Integración con modelos de embeddings de HuggingFace
- LangChain Google Genai: Integración con modelos de Google Gemini

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

## Uso de la Interfaz Web

Al acceder a http://localhost:8001 se cargará la interfaz web del chatbot donde podrás:

1. Enviar mensajes al chatbot
2. Guardar información (ej: "Guarda que la capital de Francia es París")
3. Hacer preguntas sobre la información almacenada (ej: "¿Cuál es la capital de Francia?")
4. Reiniciar la conversación con el botón correspondiente

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
  "response": {
    "query": {
      "role": "user", 
      "content": "Guarda que la capital de Francia es París"
    },
    "decided_to_save": true,
    "chat_history": [
      {
        "role": "assistant", 
        "content": "He guardado la información: la capital de Francia es París."
      }
    ],
    "context": []
  }
}
```

## Arquitectura del sistema

El proyecto utiliza una arquitectura basada en agentes con LangGraph:

1. **Decider Agent**: Analiza el mensaje del usuario y determina si es una solicitud para guardar información o una pregunta.
2. **Saver Agent**: Se activa cuando el usuario quiere guardar información en la base de conocimientos.
3. **QA Agent**: Se activa cuando el usuario hace una pregunta, consultando la base de conocimientos para proporcionar una respuesta.

El flujo de trabajo se define mediante un grafo dirigido que conecta estos agentes según la decisión tomada por el Decider Agent.

### Estructura de archivos

```
chatbot-fastapi/
├── app/
│   ├── static/
│   │   ├── index.html      # Página web principal
│   │   ├── script.js       # Lógica del frontend
│   │   └── styles.css      # Estilos CSS
│   └── models/             # Modelos adicionales (si los hay)
├── chat_service.py         # Lógica de los agentes y grafo de trabajo
├── main.py                 # Endpoints de FastAPI
└── requirements.txt        # Dependencias del proyecto
```

## Notas de implementación

- **Frontend generado por IA**: La interfaz de usuario fue completamente generada por Cursor AI a partir de un prompt, demostrando el potencial de las herramientas de IA para el desarrollo rápido de interfaces.

- **Enfoque en la IA**: Como parte de un curso educativo de IA para programadores, este proyecto se centra principalmente en la implementación de conceptos relacionados con la IA (agentes, orquestación, RAG) más que en aspectos de ingeniería de software robusta.

- **Código educativo**: El código está diseñado para ser legible y comprensible, pero no incluye todas las prácticas recomendadas para entornos de producción (como manejo exhaustivo de errores con bloques try-except, validaciones completas, etc.).

## Contribuciones

Las mejoras a este proyecto son bienvenidas a través de pull requests. Algunas áreas que podrían beneficiarse de contribuciones incluyen:

- Mejora del manejo de errores
- Implementación de pruebas unitarias
- Optimización del rendimiento de las búsquedas vectoriales
- Mejoras en la interfaz de usuario
- Adición de funcionalidades como exportación/importación de la base de conocimientos

## Contexto educativo

Este proyecto es parte del curso **"IA para programadores"**, diseñado para enseñar cómo integrar modelos de lenguaje en aplicaciones prácticas mediante el uso de LangChain y LangGraph dentro de un entorno web con FastAPI. 