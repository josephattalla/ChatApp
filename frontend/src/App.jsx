import { createContext, useState } from 'react'
import './App.css'

import LoginPage from './LoginPage';
import ChatPage from "./ChatPage";

export const AuthContext = createContext(null);

export function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [sessionToken, setSessionToken] = useState(null);
  const [username, setUsername] = useState("");
  const [userId, setUserId] = useState("");

  return (
    <>
      {authenticated ? (
        <AuthContext.Provider>
          <ChatPage />
        </AuthContext.Provider>
      ): (
        // useContext is overkill for LoginPage until React Router impl
        <AuthContext.Provider value={{ setAuthenticated, setSessionToken, setUsername, setUserId }}>
          <LoginPage />
        </AuthContext.Provider>
      )}
    </>
  )
}
