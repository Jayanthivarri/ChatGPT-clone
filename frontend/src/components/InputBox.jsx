import { useState } from "react";
import api from "../services/api";

function InputBox({ messages, setMessages }) {
  const [text, setText] = useState("");

  const sendMessage = async () => {
    if (!text.trim()) return;

    // Show user message immediately
    const userMessage = {
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const token = localStorage.getItem("token");

      const response = await api.post(
        "/chat",
        {
          session_id: null,
          message: text,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const aiMessage = {
        role: "assistant",
        content: response.data.response,
      };

      setMessages((prev) => [...prev, aiMessage]);

      setText("");
    } catch (error) {
      console.log(error);
      console.log(error.response);
      console.log(error.response?.data);

      alert(JSON.stringify(error.response?.data || error.message));

      setText("");
    }
  };

  return (
    <div className="input-box">
      <input
        type="text"
        placeholder="Message ChatGPT..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            sendMessage();
          }
        }}
      />

      <button onClick={sendMessage}>➤</button>
    </div>
  );
}

export default InputBox;