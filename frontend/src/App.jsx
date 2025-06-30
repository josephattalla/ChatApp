import { useState } from 'react'
import './App.css'

import LoginPage from './LoginPage';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  return (
    <>
      <h1>ChatApp</h1>
      {authenticated ? (
        <h1>Successfully authenticated</h1>
      ): (
        <LoginPage onChange={ setAuthenticated } />
      )}
    </>
  )
}

export default App
