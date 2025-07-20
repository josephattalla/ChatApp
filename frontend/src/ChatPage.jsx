import { useState, useContext, useEffect } from "react";
import { AuthContext } from "./App";

import Sidebar from "./Sidebar";
import ChatContent from "./ChatContent";
import "./ChatPage.css";

export default function ChatPage({ setSelectedPage }) {
  const [sessionId, setSessionId] = useState(null);
  const [rooms, setRooms] = useState([]);
  // RoomID is selected before being able to fetch to SessionID.
  // This causes ChatContent to use an invalid Session ID upon rerendering on a
  // new RoomID. Solution: User chosen RoomID is marked pending and only set as
  // the true RoomID when the SessionID is available.
  const [pendingRoomId, setPendingRoomId] = useState(null);
  const [selectedRoomId, setSelectedRoomId] = useState(null);
  const { setAuthenticated, accessToken, username, userId } = useContext(AuthContext);

  useEffect(function getSessionId() {
    if (pendingRoomId === null) {
      return;
    }
    setSessionId(null);

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
      setSelectedRoomId(pendingRoomId);
    })
    .catch(function(error) {
      console.log(error.message);
      // Reenter credentials if session id fetch fails.
      setAuthenticated(false);
    });
  }, [pendingRoomId]);

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

  // Immediately stop ChatContent from rendering while fetching new SessionId.
  function handleRoomPick(roomId) {
    if (roomId !== pendingRoomId) {
      setPendingRoomId(roomId);
      setSelectedRoomId(null);
    }
  }

  let renderedChatContent;
  let selectedRoom;
  if (selectedRoomId) {
    selectedRoom = rooms.find(room => room.room_id === selectedRoomId);
    renderedChatContent = (
      // setting a key forces remount on new room, causing the websocket to close
      <ChatContent
        key={selectedRoomId}
        sessionId={sessionId}
        selectedRoom={selectedRoom}
      />
    )
  } else if (pendingRoomId) {
    renderedChatContent = <h1>Loading Room</h1>;
  } else {
    renderedChatContent = <h1>No Room Selected</h1>;
  }

  return (
    <div className="chatpage-body">
      <div className="app-content">
        <header className="chatpage-header">
          <h1 className="server-name">{selectedRoom?.room_name ?? ""}</h1>
          <button onClick={() => setSelectedPage("settings")}>
            Settings
          </button>
        </header>
        <Sidebar rooms={rooms} handleRoomPick={handleRoomPick} />
        {renderedChatContent}
      </div>
    </div>
  )
}
