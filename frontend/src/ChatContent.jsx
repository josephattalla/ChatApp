import { useEffect, useContext, useState } from "react"
import useWebSocket from "react-use-websocket";
import { AuthContext } from "./App";
import ChatBox from "./ChatBox";

export default function ChatContent({ sessionId, selectedRoom }) {
  const { userRole, setAuthenticated, accessToken, userId } = useContext(AuthContext);
  const [roomMessages, setRoomMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const WS_URL = `ws://localhost:8000/ws/${selectedRoom.room_id}`;
  const {
    sendJsonMessage,
    lastJsonMessage,
  } = useWebSocket(
    WS_URL,
    {
      queryParams: {
        user_id: userId,
        session_id: sessionId,
      },
      share: true,
      retryOnError: false,
    },
  );

  useEffect(function() {
    if (lastJsonMessage?.type === "room messages") {
      setRoomMessages(lastJsonMessage.messages);
    } else if (lastJsonMessage?.type === "new chat") {
      setRoomMessages([...roomMessages, {
        username: lastJsonMessage.username,
        chat: lastJsonMessage.chat,
      }])

    }
  }, [lastJsonMessage]);

  function delegatedDeleteHandler(event) {
    if (event.target.tagName === "BUTTON") {
      const chatId= event.target.closest("article").dataset.chatId;
      setLoading(true)
      fetch(`http://localhost:8000/api/rooms/${selectedRoom.room_id}/${chatId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      })
      .then(function(response) {
        if (!response.ok) {
          throw new Error("Delete failed");
        }
        return response.json();
      })
      .then(function(json) {
        setRoomMessages(
            roomMessages.filter(({ chat }) => chat.chat_id !== json.chat_id)
        );
      })
      .catch(function(error) {
        console.log(error.message);
        setAuthenticated(false);
      })
      .finally(function() {
        setLoading(false);
      })
    }
  }

  let messageDeleteButton = null;
  if (userRole === "Admin" || userRole === "Mod") {
     messageDeleteButton = (
      <button
        disabled={loading}
      >
        Delete
      </button>
    );
  }

  const renderedMessages = roomMessages.map(function({ username, chat }) {
    return (
      <article
        key={chat.chat_id}
        data-user-id={chat.user_id}
        data-chat-id={chat.chat_id}
      >
        <h3>{username} ({chat.time}) {messageDeleteButton}</h3>
        <p>{chat.message}</p>
      </article>
    )
  });

  return (
    <main className="chat-content">
      <section
        className="messages-container"
        onClick={delegatedDeleteHandler}
      >
        {renderedMessages}
      </section>
      <ChatBox
        roomMessages={roomMessages}
        setRoomMessages={setRoomMessages}
        roomId={selectedRoom.room_id}
      />
    </main>
  )
}
