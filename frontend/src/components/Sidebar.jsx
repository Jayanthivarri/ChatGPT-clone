import { useEffect, useState } from "react";
import { Trash2 } from "lucide-react";
import api from "../services/api";

function Sidebar({
  currentSession,
  setCurrentSession,
  messages,
  setMessages,
}) {
  const [sessions, setSessions] = useState([]);
  const [username, setUsername] = useState("");
  const [showMenu, setShowMenu] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, []);

  useEffect(() => {
    fetchSessions();
  }, [currentSession]);

  const fetchSessions = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get("/sessions", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setSessions(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get("/profile", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setUsername(response.data.username);
    } catch (error) {
      console.error(error);
    }
  };

  const createSession = () => {
    setCurrentSession(null);
    setMessages([]);
  };

  const loadSession = async (sessionId) => {
    try {
      const token = localStorage.getItem("token");

      const response = await api.get(`/sessions/${sessionId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setCurrentSession(sessionId);
      setMessages(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const deleteSession = async (sessionId) => {
    if (!window.confirm("Delete this chat?")) return;

    try {
      const token = localStorage.getItem("token");

      await api.delete(`/sessions/${sessionId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (currentSession === sessionId) {
        setCurrentSession(null);
        setMessages([]);
      }

      fetchSessions();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="sidebar">
      <button
        className="new-chat-btn"
        onClick={createSession}
      >
        + New Chat
      </button>

      <div className="chat-history">
        {sessions.length === 0 ? (
          <p>No Chats</p>
        ) : (
          sessions.map((session) => (
            <div
              key={session.id}
              className={`chat-item ${
                currentSession === session.id ? "active" : ""
              }`}
            >
              <span
                className="chat-title"
                onClick={() => loadSession(session.id)}
              >
                {session.title}
              </span>

              <Trash2
                size={16}
                className="delete-icon"
                onClick={() => deleteSession(session.id)}
              />
            </div>
          ))
        )}
      </div>

      <div className="profile">
        <div
          className="profile-header"
          onClick={() => setShowMenu(!showMenu)}
        >
          <div className="profile-avatar">
            {username
              ? username
                  .split(" ")
                  .map((word) => word[0])
                  .join("")
                  .slice(0, 2)
                  .toUpperCase()
              : "U"}
          </div>

          <div className="profile-info">
            <div className="profile-name">{username}</div>
          </div>

          <div className="menu-icon">⋯</div>
        </div>

        {showMenu && (
          <div className="profile-menu">
            <div className="menu-item">👤 Profile</div>

            <div className="menu-item">⚙️ Settings</div>

            <div
              className="menu-item logout"
              onClick={() => {
                localStorage.removeItem("token");
                window.location.href = "/login";
              }}
            >
              🚪 Logout
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Sidebar;