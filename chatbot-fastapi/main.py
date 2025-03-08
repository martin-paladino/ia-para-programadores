from fastapi import FastAPI, Body
from typing import Any
from chat_service import process_message

app = FastAPI(title="Chat API")

@app.get("/")
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