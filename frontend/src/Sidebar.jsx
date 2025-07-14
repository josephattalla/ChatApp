import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./App";

export default function Sidebar({ sessionId }) {
  const { setAuthenticated, accessToken } = useContext(AuthContext);
  const [rooms, setRooms] = useState([]);

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

  const groupList = rooms.map(function({ room_id, room_name }) {
    return <li key={room_id}>{room_name}</li>
  });

  return (
    <aside className="sidebar">
      <h2 className="sidebar-title">Groups</h2>
      <ul className="group-list">
        {groupList}
      </ul>
    </aside>
  )
}
