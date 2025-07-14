import { useState, useContext, useEffect } from "react";
import { AuthContext } from "./App";

import Sidebar from "./Sidebar";
import "./ChatPage.css";

export default function ChatPage() {
  // sessionId for connecting to websocket
  const [sessionId, setSessionId] = useState(null);
  const [rooms, setRooms] = useState([]);
  const [selectedRoomId, setSelectedRoomId] = useState(null);
  const { setAuthenticated, accessToken, username, userId } = useContext(AuthContext);

  useEffect(function getSessionId() {
    // Acquire session id by providing access token
    fetch("http://localhost:8000/api/session", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    })
    .then(function(response) {
      if (response.status === 401) {
        throw new Error("Unauthorized: Retrying login");
      }
      return response.json();
    })
    .then(function(json) {
      setSessionId(json.session_id);
    })
    .catch(function(error) {
      console.log(error.message);
      // Reenter credentials if session id fetch fails.
      setAuthenticated(false);
    });
  }, []);

  useEffect(function getGroups() {
    fetch("http://localhost:8000/api/rooms", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json",
      },
    })
    .then(function(response) {
      if (response.status === 401) {
        throw new Error("Unauthorized: Retrying login");
      }
      return response.json();
    })
    .then(function(json) {
      setRooms(json.rooms);
    })
    .catch(function(error) {
      console.log(error.message);
      // Reenter credentials if session id fetch fails.
      setAuthenticated(false);
    });
  }, []);

  return (
    <div className="chatpage-body">
      <div className="app-content">
        <header className="chatpage-header">
          <h1 className="server-name">Server name</h1>
          <button>Profile</button>
        </header>
        <Sidebar rooms={rooms} setSelectedRoomId={setSelectedRoomId} />
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
      </div>
    </div>
  )
}
