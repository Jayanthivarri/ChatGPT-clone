function Sidebar() {
  return (
    <div className="sidebar">
      <button className="new-chat-btn">
        + New Chat
      </button>

      <div className="chat-history">
        <p>Chat 1</p>
        <p>Chat 2</p>
        <p>Chat 3</p>
      </div>

      <div className="profile">
        👤 Jayanthi
      </div>
    </div>
  );
}

export default Sidebar;