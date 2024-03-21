
const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const navBtn = document.querySelector(".btn-nav")


let userMessage = null; // Variable to store user's message
const inputInitHeight = chatInput.scrollHeight;


// Script.js

let tokenJWT;


function test() {
  const url = 'https://esva-demo-soel3q6bbq-uw.a.run.app/test';


  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Error en la solicitud');
      }
      return response.json();
    })
    .then(data => {
      console.log('Respuesta de la API sin Token:', data);
      // Aquí puedes manejar la respuesta de la API como desees
    })
    .catch(error => {
      console.error('Error al consultar la API sin Token:', error);
    });
}

function login() {
  const url = 'https://esva-demo-soel3q6bbq-uw.a.run.app/api/login';
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const credentials = {
    username: username,
    password: password
  };

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  };
  // console.log(url, options)
  fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error('Error en la solicitud');
      }
      return response.text(); // Obtener el texto de la respuesta
    })
    .then(text => {
      tokenJWT = text.trim(); // Asignar el token a la variable global, eliminando espacios en blanco
      console.log('Token JWT:', tokenJWT);
      document.getElementById("successfullLogin").style.display = "block" ;
      document.getElementById("loginForm").style.display = "none";
      // Aquí puedes manejar el token JWT como desees
    })
    .catch(error => {
      document.getElementById("warningLogin").style.display = "block" ;
      console.error('Error al consultar la API sin Token:', error);
    });
}

function imprimirJWT() {
  console.log(tokenJWT)
}

function testToken() {
  const url = 'https://esva-demo-soel3q6bbq-uw.a.run.app/api/verify/token';

  const options = {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${tokenJWT}`
    }
  };

  fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error('Error en la solicitud');
      }
      return response.json();
    })
    .then(data => {
      console.log('Respuesta de la API con Token:', data);
      // Aquí puedes manejar la respuesta de la API como desees
    })
    .catch(error => {
      console.error('Error al consultar la API con Token:', error);
    });
}

function makeQuestion(query) {
  const url = 'https://esva-demo-soel3q6bbq-uw.a.run.app/api/getAnswer';

  const credentials = {
    query: query
  };

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${tokenJWT}`
    },
    body: JSON.stringify(credentials)
  };

  fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error('Error en la solicitud');
      }
      return response.json();
    })
    .then(data => {
      console.log('Respuesta de la API con Token:', data);
      // Aquí puedes manejar la respuesta de la API como desees
    })
    .catch(error => {
      console.error('Error al consumir la API con Token:', error);
    });
}

function encontrarCoincidencia(cadena) {
  // Normaliza la cadena de entrada eliminando espacios y convirtiendo a minúsculas
  var normalizedInput = cadena.trim().toLowerCase();
  // Itera sobre las claves del objeto data
  for (var key in data) {
    // Normaliza la clave eliminando espacios y convirtiendo a minúsculas
    var normalizedKey = key.trim().toLowerCase();
    // Verifica si la cadena normalizada coincide con la clave normalizada
    if (normalizedKey.includes(normalizedInput)) {
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
  const url = 'https://esva-demo-soel3q6bbq-uw.a.run.app/api/getAnswer';

  const credentials = {
    query: queryString
  };

  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${tokenJWT}`
    },
    body: JSON.stringify(credentials)
  };

  fetch(url, options)
    .then(response => response.json())
    .then(json => {
      response = json["message"]
      if (response == "Invalid Token") {
        messageElement.textContent = "por favor, inicie sesión para validar que es un usuario autenticado"
      } else {
        messageElement.textContent = json["message"];
      }

    })
    .catch(error => {
      console.error('Error al consumir la API con Token:', error);
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
    // cambia el mensaje de buscando respuesta por la respuesta del elemento
    generateResponse(incomingChatLi);
  }, 600);
};

// parte de codgo unicamente utilizada para que el chat registre la pregunta con la tecla enter
// 
document.addEventListener("DOMContentLoaded", function () {
  const textarea = document.querySelector(".chat-input textarea");
  const sendButton = document.getElementById("send-btn");
  textarea.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Evita que se haga un salto de línea en el textarea
      sendButton.click(); // Simula el clic en el botón "send"
    }
  });
});

const mensaje = document.getElementById('chatAndInfo');

document.getElementById('btn-nav').addEventListener('change', function () {
  if (this.checked) {
    console.log("menu abierto")
    mensaje.style.paddingLeft = '200px';
    mensaje.classList.add('mensaje-con-transicion'); // Agrega la clase para activar la transición

  } else {
    console.log("menu cerrado")
    mensaje.style.paddingLeft = '0px';
    mensaje.classList.add('mensaje-con-transicion'); // Agrega la clase para activar la transición

  }
});

sendChatBtn.addEventListener("click", handleChat);

