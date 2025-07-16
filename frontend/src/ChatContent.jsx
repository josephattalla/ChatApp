import { useEffect, useRef, useContext } from "react"
import useWebSocket, { ReadyState } from "react-use-websocket";
import { AuthContext } from "./App";

export default function ChatContent({ sessionId, selectedRoom }) {
  const { setAuthenticated, accessToken, userId } = useContext(AuthContext);
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
    if (lastJsonMessage) {
      console.log(lastJsonMessage);
    }
  }, [lastJsonMessage]);

  return (
    <main className="chat-content">
      <div className="messages-container">
        <div className="message">Messages go here</div>
        <div className="message">Messages go here</div>
        <div className="message">Messages go here</div>
        <div className="message">Messages go here</div>
      </div>
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
