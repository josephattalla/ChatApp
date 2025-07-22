import { useContext, useState } from "react"
import { AuthContext } from "./App";

export default function ChatBox({ roomId }) {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const { setAuthenticated, accessToken } = useContext(AuthContext);

  function sendMessage() {
    setLoading(true);

    fetch(`http://localhost:8000/api/rooms/${roomId}`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message.trim(),
      }),
    })
    .catch(function(error) {
      console.log(error.message);
      setAuthenticated(false);
    })
    .finally(function() {
      setLoading(false)
      setMessage("");
    });
  }

  function handleEnterKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      if (!message.trim()) {
        return;
      }
      event.preventDefault();
      sendMessage();
    }
  }

  return (
    <form action="" className="chatbox">
      <textarea
        id="chat-textarea"
        className="chat-textarea"
        placeholder="Type away..."
        onChange={event => setMessage(event.target.value)}
        onKeyDown={handleEnterKeydown}
        value={message}
        disabled={loading}
      />
    </form>
  )
}
