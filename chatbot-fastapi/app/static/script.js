document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const restartButton = document.getElementById('restart-button');
    const welcomeMessage = document.querySelector('.welcome-message');
    
    // URL del backend
    const API_URL = 'http://localhost:8001/chat';
    
    // Mensaje de bienvenida inicial
    const WELCOME_MESSAGE = '¡Hola! Soy tu asistente IA. ¿En qué puedo ayudarte hoy?';
    
    // Historial de mensajes
    let messages = [{
        role: 'assistant',
        content: WELCOME_MESSAGE
    }];
    
    const userName = "Usuario"; // Valor hardcodeado para este ejemplo
    
    // Configurar saludo personalizado
    setWelcomeMessage();
    
    // Mostrar el mensaje inicial
    addMessageToUI(WELCOME_MESSAGE, 'bot');
    
    // Función para mostrar saludo personalizado
    function setWelcomeMessage() {
        const hora = new Date().getHours();
        let saludo = "Buenos días";
        
        if (hora >= 12 && hora < 20) {
            saludo = "Buenas tardes";
        } else if (hora >= 20 || hora < 6) {
            saludo = "Buenas noches";
        }
        
        welcomeMessage.textContent = `${saludo}, ${userName}`;
    }
    
    // Funcionalidad para reiniciar el chat
    restartButton.addEventListener('click', () => {
        resetChat();
    });
    
    // Función para reiniciar el chat
    function resetChat() {
        // Reiniciar el historial de mensajes
        messages = [{
            role: 'assistant',
            content: WELCOME_MESSAGE
        }];
        
        // Limpiar el chat en la UI
        chatMessages.innerHTML = '';
        
        // Añadir mensaje de bienvenida
        addMessageToUI(WELCOME_MESSAGE, 'bot');
        
        // Limpiar el input del usuario
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Animación del botón
        restartButton.classList.add('rotating');
        setTimeout(() => {
            restartButton.classList.remove('rotating');
        }, 500);
    }
    
    // Funcionalidad para enviar mensaje con Enter
    userInput.addEventListener('keydown', (e) => {
        // Enter sin Shift envía el mensaje
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
        
        // Ajustar altura del textarea automáticamente
        setTimeout(() => {
            adjustTextareaHeight();
        }, 0);
    });
    
    // Input dinámico que se ajusta al contenido
    function adjustTextareaHeight() {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 150) + 'px';
    }
    
    // Manejar click en botón enviar
    sendButton.addEventListener('click', sendMessage);
    
    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;
        
        // Agregar mensaje del usuario al historial
        messages.push({
            role: 'user',
            content: message
        });
        
        // Mostrar mensaje del usuario en la interfaz
        addMessageToUI(message, 'user');
        
        // Limpiar input
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Mostrar indicador de escritura
        showTypingIndicator();
        
        // Hacer la petición al backend
        fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ messages: messages })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(data => {
            // Ocultar indicador de escritura
            hideTypingIndicator();
            
            // Procesar respuesta
            if (data.response && data.response.chat_history && data.response.chat_history.length > 0) {
                // Obtener el último mensaje de la respuesta
                const lastMessage = data.response.chat_history[data.response.chat_history.length - 1];
                
                // Actualizar el historial completo
                messages = data.response.chat_history;
                
                // Mostrar la respuesta en la interfaz
                addMessageToUI(lastMessage.content, 'bot');
            } else {
                // Manejar respuesta inesperada
                console.error('Respuesta inesperada del servidor:', data);
                addMessageToUI('Lo siento, ha ocurrido un error al procesar tu solicitud.', 'bot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            hideTypingIndicator();
            addMessageToUI('Lo siento, ha ocurrido un error al comunicarse con el servidor.', 'bot');
        });
    }
    
    // Agregar mensaje al UI
    function addMessageToUI(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageParagraph = document.createElement('p');
        messageParagraph.textContent = content;
        
        messageContent.appendChild(messageParagraph);
        messageDiv.appendChild(messageContent);
        
        // Agregar tiempo del mensaje
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = getCurrentTime();
        messageDiv.appendChild(timeDiv);
        
        chatMessages.appendChild(messageDiv);
        
        // Scroll al último mensaje
        scrollToBottom();
    }
    
    // Mostrar indicador de "escribiendo..."
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message';
        typingDiv.id = 'typing-indicator';
        
        const typingContent = document.createElement('div');
        typingContent.className = 'message-content typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingContent.appendChild(dot);
        }
        
        typingDiv.appendChild(typingContent);
        chatMessages.appendChild(typingDiv);
        
        scrollToBottom();
    }
    
    // Ocultar indicador de "escribiendo..."
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Obtener hora actual formateada
    function getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
    
    // Scroll al final del chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Inicializar la altura del textarea
    adjustTextareaHeight();
}); 