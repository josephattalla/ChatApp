import { useContext, useState } from "react";
import { AuthContext } from "./App";

export default function Sidebar({ rooms, handleRoomPick, getGroups }) {
  const { setAuthenticated, accessToken, userRole } = useContext(AuthContext);
  const [newRoomName, setNewRoomName] = useState("");
  const [loading, setLoading] = useState(false);
  const groupList = rooms.map(function({ room_id, room_name }) {
    return (
      <li
        key={room_id}
        data-room-id={room_id}
      >
        {room_name}
      </li>
    );
  });

  function groupListClickHandler(event) {
    const selectedId = Number(event.target.dataset.roomId);
    if (!Number.isNaN(selectedId)) {
      handleRoomPick(selectedId);
    }
  };

  function addRoom() {
    setLoading(true);
    fetch(
      "http://localhost:8000/api/mod/room?" + new URLSearchParams({
        room_name: newRoomName.trim(),
      }),
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
        },
      }
    )
    .then(function(response) {
      return response.json();
    })
    .then(function(_) {
      getGroups();
    })
    .catch(function(error) {
      console.log(error.message);
      setAuthenticated(false);
    })
    .finally(function() {
      setLoading(false)
      setNewRoomName("");
    });
  }

  return (
    <aside className="sidebar">
      <h2 className="sidebar-title">Groups</h2>
      <ul
        className="group-list"
        onClick={groupListClickHandler}
      >
        {groupList}
      </ul>
      {(userRole === "Admin") &&
        <form action={addRoom}>
          <input
            id="new-room-name"
            value={newRoomName}
            onChange={event => setNewRoomName(event.target.value)}
            placeholder="New room name"
            readOnly={loading}
            type="text"
            minLength={1}
            maxLength={20}
            required={true}
          />
          <button>{loading ? "Loading" : "Add"}</button>
        </form>
      }
    </aside>
  )
}
