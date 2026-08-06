import { useState } from "react";

import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

function Chat() {

  const [currentSession, setCurrentSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isThinking, setIsThinking] = useState(false);
  return (
    <div className="chat-container">

      <Sidebar
        currentSession={currentSession}
        setCurrentSession={setCurrentSession}
        messages={messages}
        setMessages={setMessages}
      />

      <ChatWindow
        currentSession={currentSession}
        setCurrentSession={setCurrentSession}
        messages={messages}
        setMessages={setMessages}
        isThinking={isThinking}
        setIsThinking={setIsThinking}
      />

    </div>
  );
}

export default Chat;