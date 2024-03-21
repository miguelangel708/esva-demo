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
                document.getElementById("loginContainer").style.display = "none";

                // console.log('Token JWT:', tokenJWT);
                // Aquí puedes manejar el token JWT como desees
            })
            .catch(error => {
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
