from fastapi import FastAPI, Body
from typing import Any
from chat_service import process_message
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os

app = FastAPI(title="Chat API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las orígenes en desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

# Montar archivos estáticos
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_chat_page():
    """
    Sirve la página HTML del chat
    """
    html_file = os.path.join(static_dir, "index.html")
    return FileResponse(html_file)

@app.get("/api")
def root():
    return {"message": "Bienvenido a la API de Chat"}

@app.post("/chat")
def chat(data: Any = Body(...)):
    """
    Endpoint para procesar mensajes de chat
    """
    response = process_message(data)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
