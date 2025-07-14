export default function Sidebar({ rooms, setSelectedRoomId }) {
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
      setSelectedRoomId(selectedId);
    }
  };

  return (
    <aside className="sidebar">
      <h2 className="sidebar-title">Groups</h2>
      <ul
        className="group-list"
        onClick={groupListClickHandler}
      >
        {groupList}
      </ul>
    </aside>
  )
}
