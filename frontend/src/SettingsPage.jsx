import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./App";

export default function SettingsPage({ setSelectedPage }) {
  const [users, setUsers] = useState([]);
  const {
    setAuthenticated,
    accessToken,
    username,
    userRole,
  } = useContext(AuthContext);

  useEffect(function getUsers() {
    if (userRole === "Admin") {
      fetch("http://localhost:8000/api/admin/users", {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      })
      .then(function(response) {
        return response.json();
      })
      .then(function(json) {
        setUsers(json.users);
      })
      .catch(function(error) {
        console.log(error);
        setAuthenticated(false);
      });
    }
  }, []);

  const renderedUsers = users.map(function({ username, role, user_id }) {
    return (
      <li
        key={user_id}
        data-user-id={user_id}
      >
        <h3>{username} ({role})</h3>
      </li>
    );
  });

  return (
    <>
      <header>
        <button onClick={() => setSelectedPage("chat")}>
          Go Back
        </button>
      </header>
      <main>
        <h1>Settings</h1>
        <h2>{username} ({userRole})</h2>
        <button onClick={() => setAuthenticated(false)}>
          Logout
        </button>
        {renderedUsers}
      </main>
    </>
  );
}
