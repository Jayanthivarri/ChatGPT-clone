import { useState } from "react";
import InputBox from "./InputBox";

function ChatWindow() {
  const [messages, setMessages] = useState([]);

  return (
    <div className="chat-window">
      <div className="navbar">
        <h2>ChatGPT Clone</h2>
      </div>

      <div className="messages">
        {messages.length === 0 ? (
          <>
            <h3>Welcome 👋</h3>
            <p>How can I help you today?</p>
          </>
        ) : (
          messages.map((msg, index) => (
            <div key={index}>
              <strong>{msg.role === "user" ? "You" : "Assistant"}</strong>
              <p>{msg.content}</p>
              <br />
            </div>
          ))
        )}
      </div>

      <InputBox
        messages={messages}
        setMessages={setMessages}
      />
    </div>
  );
}

export default ChatWindow;