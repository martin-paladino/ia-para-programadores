# Chatbot FastAPI

Proyecto básico de un chatbot implementado con FastAPI.

## Requisitos

- Python 3.8+
- FastAPI
- Uvicorn

## Instalación

1. Clonar el repositorio
2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Para iniciar el servidor:

```bash
python main.py
```

O alternativamente:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en http://localhost:8000

## Endpoints

- `GET /`: Mensaje de bienvenida
- `POST /chat`: Endpoint para enviar mensajes al chatbot

### Ejemplo de uso del endpoint /chat

```bash
curl -X 'POST' \
  'http://localhost:8000/chat' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Hola, ¿cómo estás?"}'
```

## Documentación

La documentación automática de la API está disponible en:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 