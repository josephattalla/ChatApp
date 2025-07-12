import { useState, useContext } from "react";
import { AuthContext } from "./App";

export default function LoginPage() {
  const { setAuthenticated, setSessionToken, setUsername, setUserId } = useContext(AuthContext);
  const [usernameField, setUsernameField] = useState("johndoe");
  const [passwordField, setPasswordField] = useState("secret");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isRegister, setIsRegister] = useState(false);
  
  function sendRegister() {
    setLoading(true);
    fetch("http://localhost:8000/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: usernameField,
        password: passwordField,
      }),
    })
    .then(function(response) {
      switch (response.status) {
        case 401:
          throw new Error("Server error");
      }
      return response.json();
    })
    .then(function(json) {
      console.log(json);
      setIsRegister(false);
    })
    .catch(error => setError(error))
    .finally(function() {
      setLoading(false);
    })
  }

  function sendLogin() {
    setLoading(true);
    fetch("http://localhost:8000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({
        username: usernameField,
        password: passwordField,
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
      setSessionToken(json.access_token);
      setUserId(json.user_id);
      setUsername(json.username);
      setAuthenticated(true);
    })
    // handle fetch failures and login problems
    .catch(error => setError(error))
    .finally(function() {
     setLoading(false);
    })
  }

  return (
    <div>
      <h1>
        { isRegister ? "Sign up for free" : "Sign in to your account" }
      </h1>
      <form action={isRegister ? sendRegister : sendLogin}>
        <button
          type="button"
          onClick={() => setIsRegister(!isRegister)}
        >
          { isRegister ? "Sign in to your existing account" : "Sign up for a new account" }
        </button>
        <div>
          <label htmlFor="username">Username</label>
          <input
            id="username"
            value={usernameField}
            onChange={event => setUsernameField(event.target.value)}
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
            value={passwordField}
            onChange={event => setPasswordField(event.target.value)}
            readOnly={loading}
            type="text"
            required={true}
            name="password"
          />
        </div>
        { error &&
          (<h1>{error.message}</h1>)
        }
        <button type="submit">
          { 
            loading ? "Loading" : 
            isRegister ? "Sign up" : "Sign in"
          }
        </button>
      </form>
    </div>
  )
}
