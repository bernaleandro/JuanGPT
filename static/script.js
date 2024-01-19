// function sendMessage(){
//     var userMessage = document.querySelector(".user-input").value;
//     document.querySelector('.chat-log').value += `Usuario: ${userMessage}\n`;

//     fetch('/send_message',{
//         method:'POST',
//         headers:{
//             'Content-Type':'application/x-www-form-urlencoded',
//         },
//         body: 'user-input=' + encodeURIComponent(userMessage),
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Datos recibidos:', data);
//         var chatbotResponse = data['chatbot_response'];
//         document.querySelector(".chat-log").value += `Juan: ${chatbotResponse}\n`;
//     });

//     document.querySelector(".user-input").value = '';
// }

function sendMessage() {
    var userMessage = document.querySelector(".user-input").value;
    var chatLog = document.querySelector('.chat-log');

    // Crea un elemento div para el mensaje del usuario
    var userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'user-message';
    userMessageDiv.textContent = userMessage;

    // Agrega el elemento div al div de chat
    chatLog.appendChild(userMessageDiv);

    // Realiza la solicitud al servidor
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'user-input=' + encodeURIComponent(userMessage),
    })
    .then(response => response.json())
    .then(data => {
        var chatbotResponse = data['chatbot_response']; // Asegúrate de usar la clave correcta

        // Crea un elemento div para la respuesta del bot
        var botResponseDiv = document.createElement('div');
        botResponseDiv.className = 'bot-response';
        botResponseDiv.textContent = 'Juan: ' + chatbotResponse;

        // Agrega el elemento div al div de chat
        chatLog.appendChild(botResponseDiv);
    });

    // Limpia el campo de entrada del usuario
    document.querySelector(".user-input").value = '';
}






