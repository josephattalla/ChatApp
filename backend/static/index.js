let ws;

document.addEventListener("DOMContentLoaded", (_e) => {
  let idForm = document.getElementById("user-id-form");
  let chatForm = document.getElementById("chat-form");

  // when id is selected:
  //  1. validate id
  //  2. connect to websocket with id
  //  3. hide idForm, display chatForm
  idForm.addEventListener("submit", event => {
    event.preventDefault();

    let idValue = Number.parseInt(document.getElementById("user-id").value);
    if (Number.isNaN(idValue) || idValue < 0 || idValue > 100) {
      return;
    }

    // connect to websocket
    ws = new WebSocket(`ws://chatapp-postgres:8000/ws/${idValue}`);
    ws.onmessage = handleSocketMessage;

    // hide id form, show chat form
    idForm.style.display = "none";
    chatForm.style.display = "block";
  });
});

const handleMessageSubmission = (event) => {
  event.preventDefault();
  const input = document.getElementById("user-input").value;

  if (input !== "") {
    ws.send(input);
  }
}


const handleSocketMessage = (e) => {
  // add new messages to list of messages
  console.log(e.data);
  let chatList = document.getElementById("chats");
  let data = JSON.parse(e.data);
  console.log(data["chats"]);
  for (let i = 0; i < data["chats"].length; i++) {
    console.log(data["chats"][i]);
    let message = document.createElement('li');
    let content = document.createTextNode(`${data["chats"][i][0]}: ${data["chats"][i][1]}`);
    message.appendChild(content);
    chatList.appendChild(message);
  }
}
