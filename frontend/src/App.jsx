import { createContext, useState } from 'react'
import './App.css'

import LoginPage from './LoginPage';
import ChatPage from "./ChatPage";
import SettingsPage from './SettingsPage';

export const AuthContext = createContext(null);

export function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState(null);
  const [username, setUsername] = useState("");
  const [userId, setUserId] = useState("");
  const [selectedPage, setSelectedPage] = useState("");

  let renderedPage;
  if (!authenticated) {
    renderedPage = (
      <AuthContext.Provider value={{
        setAuthenticated,
        setAccessToken,
        username,
        setUsername,
        setUserId
      }}>
        <LoginPage setSelectedPage={setSelectedPage} />
      </AuthContext.Provider>
    )
  } else if (selectedPage === "chat") {
    renderedPage = (
      <AuthContext.Provider value={{ setAuthenticated, accessToken, username, userId }}>
        <ChatPage setSelectedPage={setSelectedPage} />
      </AuthContext.Provider>
    )
  } else if (selectedPage === "settings") {
    renderedPage = SettingsPage();
  } else {
    renderedPage = <p1>Something went very, very wrong here.</p1>;
  }

  return (
    <>
      {renderedPage}
    </>
  )
}
