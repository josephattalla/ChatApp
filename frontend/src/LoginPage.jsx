import { useState } from "react";

export default function LoginPage({ onChange }) {
  const [username, setUsername] = useState("johndoe");
  const [password, setPassword] = useState("secret");

  async function sendLogin() {
    const response = await fetch("http://localhost:8000/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({
        username: username,
        password: password,
      }),
    })

    if (response.status === 401) {
      console.log("nah")
    }

    response.json().then(() => onChange(true));
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
        <button type="submit">Login</button>
      </form>
    </div>
  )
}
