
const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight;

function encontrarCoincidencia(cadena) {
// Normaliza la cadena de entrada eliminando espacios y convirtiendo a minúsculas
var normalizedInput = cadena.trim().toLowerCase();
// Itera sobre las claves del objeto data
for (var key in data) {
  // Normaliza la clave eliminando espacios y convirtiendo a minúsculas
  var normalizedKey = key.trim().toLowerCase();
  // Verifica si la cadena normalizada coincide con la clave normalizada
  if (normalizedKey.includes(normalizedInput) ) {
    // Retorna la clave con la que coincidió
    return key;
  }
}
// Si no hay coincidencia, retorna null
return null;
}

const createChatLi = (message, className) => {
// Create a chat <li> element with passed message and className
const chatLi = document.createElement("li");
chatLi.classList.add("chat", `${className}`);
let chatContent =
  className === "outgoing"
    ? `<p></p>`
    : `<span><img src="https://west.net.co/wp-content/uploads/2024/01/westbot.jpeg"></span><p></p>`;
chatLi.innerHTML = chatContent;
chatLi.querySelector("p").textContent = message;
return chatLi; // return chat <li> element
};

const generateResponse = (chatElement) => {
    const messageElement = chatElement.querySelector("p");
    var queryString = userMessage;
    var encodedQueryString = encodeURIComponent(queryString);
    var apiUrl = 'http://127.0.0.1:5000/esvachatbotapi-colwest2?query=' + encodedQueryString;

    // Establecer el tiempo de espera en milisegundos (por ejemplo, 10 segundos)
    const timeoutMillis = 15000; // 10 segundos

    // Crear una promesa que se resuelve después del tiempo de espera
    const timeoutPromise = new Promise((resolve, reject) => {
        setTimeout(() => {
            reject(new Error('Tiempo de espera excedido'));
        }, timeoutMillis);
    });

    // Realizar la solicitud fetch a la API y la promesa de tiempo de espera
    Promise.race([
        fetch(apiUrl),
        timeoutPromise
    ])
    .then(response => response.json())
    .then(json => {
        console.log(json["answer"]);
        messageElement.textContent = json["answer"];
    })
    .catch(error => {
        console.error('Error:', error);
        // Manejar el error de tiempo de espera o cualquier otro error
        if (error.message === 'Tiempo de espera excedido') {
            // Puedes mostrar un mensaje al usuario indicando que la solicitud ha tardado demasiado en responder
            messageElement.textContent = 'La solicitud ha tardado demasiado en responder. Por favor, inténtalo de nuevo más tarde.';
        } else {
            // Otro tipo de error
            messageElement.textContent = 'Se ha producido un error al procesar tu solicitud.';
        }
    });
};



const handleChat = () => {
userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
if (!userMessage) return;

// Clear the input textarea and set its height to default
chatInput.value = "";
chatInput.style.height = `${inputInitHeight}px`;

// Append the user's message to the chatbox
chatbox.appendChild(createChatLi(userMessage, "outgoing"));
chatbox.scrollTo(0, chatbox.scrollHeight);

setTimeout(() => {
  const incomingChatLi = createChatLi("Buscando respuesta...", "incoming");
  chatbox.appendChild(incomingChatLi);
  chatbox.scrollTo(0, chatbox.scrollHeight);
1}, 600);
};

// parte de codgo unicamente utilizada para que el chat registre la pregunta con la tecla enter
// 
document.addEventListener("DOMContentLoaded", function () {
const textarea = document.querySelector(".chat-input textarea");
const sendButton = document.getElementById("send-btn");
textarea.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Evita que se haga un salto de línea en el textarea
    sendButton.click(); // Simula el clic en el botón "send"
  }
});
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () =>
document.body.classList.remove("show-chatbot")
);
chatbotToggler.addEventListener("click", () =>
document.body.classList.toggle("show-chatbot")
);



