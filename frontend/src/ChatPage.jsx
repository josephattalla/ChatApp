import "./ChatPage.css";

export default function ChatPage() {
  return (
    <div className="chatpage-body">
      <div className="app-content">
        <header className="chatpage-header">
          <h1 className="server-name">Server name</h1>
          <button>Profile</button>
        </header>
        <aside className="sidebar">
          <h2 className="sidebar-title">Groups</h2>
          <ul className="group-list">
            <li className="group-display">Group</li>
            <li className="group-display">Group</li>
            <li className="group-display">Group</li>
            <li className="group-display">Group</li>
            <li className="group-display">Group</li>
            <li className="group-display">Group</li>
          </ul>
        </aside>
        <main className="chat-content">
          <div className="messages-container">
            <div className="message">Messages go here</div>
            <div className="message">Messages go here</div>
            <div className="message">Messages go here</div>
            <div className="message">Messages go here</div>
          </div>
          <form action="" className="chatbox">
            <textarea
              name=""
              id="chat-textarea"
              className="chat-textarea"
              placeholder="Type away..."
            >
            </textarea>
          </form>
        </main>
      </div>
    </div>
  )
}
