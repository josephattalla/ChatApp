import { createContext, useState } from 'react'
import './App.css'

import LoginPage from './LoginPage';

export const AuthContext = createContext(null);

export function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [sessionToken, setSessionToken] = useState(null);
  const [username, setUsername] = useState("");
  const [userId, setUserId] = useState("");

  return (
    <>
      <h1>ChatApp</h1>
      {authenticated ? (
        <h1>authenticated</h1>
      ): (
        // useContext is overkill for LoginPage until React Router impl
        <AuthContext.Provider value={{ setAuthenticated, setSessionToken, setUsername, setUserId }}>
          <LoginPage />
        </AuthContext.Provider>
      )}
    </>
  )
}
