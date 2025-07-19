import { useEffect, useContext, useState } from "react"
import useWebSocket from "react-use-websocket";
import { AuthContext } from "./App";

export default function ChatContent({ sessionId, selectedRoom }) {
  const { setAuthenticated, accessToken, userId } = useContext(AuthContext);
  const [roomMessages, setRoomMessages] = useState([]);
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
    }
  }, [lastJsonMessage]);

  const renderedMessages = roomMessages.map(function({ username, chat }) {
    return (
      <article
        key={chat.chat_id}
        data-user-id={chat.user_id}
        data-chat-id={chat.chat_id}
      >
        <h3>{username} ({chat.time})</h3>
        <p>{chat.message}</p>
      </article>
    )
  });

  return (
    <main className="chat-content">
      <section className="messages-container">
        {renderedMessages}
      </section>
      <form action="" className="chatbox">
        <textarea
          name=""
          id="chat-textarea"
          className="chat-textarea"
          placeholder="Type away..."
        >
        </textarea>
      </form>
    </main>
  )
}
