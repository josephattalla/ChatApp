import { useState } from "react";

export default function LoginPage({ onAuthenticated }) {
  const [username, setUsername] = useState("johndoe");
  const [password, setPassword] = useState("secret");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function sendLogin() {
    setLoading(true);
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
      onAuthenticated(true);
    })
    // handle fetch failures and login problems
    .catch(error => setError(error))
    .finally(function() {
     setLoading(false);
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
            value={username}
            onChange={event => setUsername(event.target.value)}
            readOnly={loading}
            type="text"
            required={true}
            name="username"
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            id="password"
            value={password}
            onChange={event => setPassword(event.target.value)}
            readOnly={loading}
            type="text"
            required={true}
            name="password"
          />
        </div>
        { error &&
          (<h1>{error.message}</h1>)
        }
        <button type="submit">{ loading ? "Loading" : "Login" }</button>
      </form>
    </div>
  )
}
