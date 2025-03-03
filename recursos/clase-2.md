# Clase 2: APIs de Modelos de Lenguaje y Asistentes de Programación

## APIs de Modelos de Lenguaje

Las APIs de modelos de lenguaje son interfaces que nos permiten interactuar con modelos de IA a través de código. Las principales opciones son:

### Google Gemini
- [Documentación de la API](https://ai.google.dev/gemini-api/docs?hl=es-419)
- [Obtener API Key](https://aistudio.google.com/apikey)
- Ofrece un plan gratuito con límites de requests
- Modelo multimodal que puede procesar texto e imágenes
- Buena opción para comenzar debido a su capa gratuita

### Anthropic Claude
- [Documentación de la API](https://docs.anthropic.com/en/api/getting-started)
- Modelo conocido por su capacidad de razonamiento y análisis detallado
- Bueno para tareas que requieren pensamiento profundo y respuestas estructuradas

### OpenAI
- [Documentación de la API](https://platform.openai.com/docs/quickstart)
- Ofrece varios modelos incluyendo GPT-4o y o1
- Amplia adopción y buena documentación
- Excelente para tareas generales de procesamiento de lenguaje

**Nota importante**: Todas estas APIs tienen costos asociados, aunque Google Gemini ofrece un plan gratuito con límites de uso. Es importante revisar los precios y límites en sus respectivas páginas web antes de comenzar a utilizarlas.

## Asistentes de Programación

### GitHub Copilot
[GitHub Copilot](https://github.com/features/copilot) es un asistente de programación impulsado por IA que se integra directamente en tu editor de código. Sus características principales incluyen:

- Sugerencias de código en tiempo real mientras escribís
- Completado automático de funciones y bloques de código
- Explicación de código existente
- Generación de tests
- Soporte para múltiples lenguajes de programación

#### Modalidades de uso:
1. **Copilot Chat**: Interfaz de chat para hacer preguntas sobre código
2. **Copilot in Editor**: Sugerencias en tiempo real mientras programas
3. **Copilot CLI**: Interfaz de línea de comandos para interacciones rápidas

#### Proyecto de ejemplo
Para practicar con Copilot, podés clonar el repositorio de la [Todo List API](https://github.com/pixegami/todo-list-api). Este proyecto es ideal para:
- Explorar el código y hacer preguntas a Copilot sobre su funcionamiento
- Practicar la generación de nuevas características
- Entender cómo Copilot puede ayudar en el desarrollo

Para clonar el repositorio, ejecutá:
```bash
git clone https://github.com/pixegami/todo-list-api.git
```

## Herramientas Adicionales

### Google Colab
[Google Colab](https://colab.google/) es un entorno de desarrollo basado en Jupyter Notebooks que:
- No requiere configuración inicial
- Ofrece acceso gratuito a recursos computacionales
- Incluye GPUs y TPUs para tareas de machine learning
- Es ideal para experimentar con código rápidamente
- Permite compartir y colaborar en notebooks
