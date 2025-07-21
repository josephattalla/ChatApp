import { useContext, useEffect, useState } from "react";
import { AuthContext } from "./App";
import AdminViewUsersListing from "./AdminViewUsersListing";

export default function SettingsPage({ setSelectedPage }) {
  const [users, setUsers] = useState([]);
  const {
    setAuthenticated,
    accessToken,
    username,
    userId,
    userRole,
  } = useContext(AuthContext);

  useEffect(function() {
    getUsers();
  }, []);

  function getUsers() {
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
        setUsers(json.users.sort((userA, userB) => {
          const usernameA = userA.username.toLowerCase()
          const usernameB = userB.username.toLowerCase()
          if (usernameA < usernameB) {
            return -1;
          } else if (usernameA > usernameB) {
            return 1;
          } else {
            return 0;
          }
        }))
      })
      .catch(function(error) {
        console.log(error);
        setAuthenticated(false);
      });
    }
  }

  /* List all users but self and display buttons to change their roles. */
  const renderedUsers = users
      .filter(({ user_id: listUserId }) => listUserId != userId)
      .map(({ username, role, user_id: userId }) => {
        return (
          <AdminViewUsersListing
            key={userId}
            username={username}
            role={role}
            userId={userId}
            onChange={getUsers}
          />
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
        <h2>Logged in: {username} ({userRole})</h2>
        <button onClick={() => setAuthenticated(false)}>
          Logout
        </button>
        { userRole === "Admin" &&
          <div>
            <h2>Current Users:</h2>
            <ul>
              {renderedUsers}
            </ul>
          </div>
        }
      </main>
    </>
  );
}
