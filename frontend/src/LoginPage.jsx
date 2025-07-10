import { useState } from "react";

export default function LoginPage({ onChange }) {
  const [username, setUsername] = useState("johndoe");
  const [password, setPassword] = useState("secret");
  const [error, setError] = useState(null);

  function sendLogin() {
    console.log("Start loading")
    fetch("http://localhost:8000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({
        username: username,
        password: password,
      }),
    })
    .then(function(response) {
      switch (response.status) {
        case 401:
          throw new Error("Bad Credentials");
      }
      return response.json();
    })
    .then(function(json) {
      onChange(true);

    })
    // handle fetch failures and login problems
    .catch(error => setError(error))
    .finally(function() {
      console.log("End loading")
    })
  }

  return (
    <div>
      <h1>Login</h1>
      <form action={sendLogin}>
        <div>
          <label htmlFor="username">Username</label>
          <input
            id="username"
            onChange={event => setUsername(event.target.value)}
            defaultValue="johndoe"
            type="text"
            name="username"
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            defaultValue="secret"
            onChange={event => setPassword(event.target.value)}
            type="text"
            name="password"
          />
        </div>
        { error &&
          (<h1>{error.message}</h1>)
        }
        <button type="submit">Login</button>
      </form>
    </div>
  )
}
