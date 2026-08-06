import { useState } from "react";
import api from "../services/api";

function InputBox({
  currentSession,
  setCurrentSession,
  messages,
  setMessages,
  isThinking,
  setIsThinking
}) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const prompt = text.trim();

    if (!prompt || loading) return;

    // Show user message immediately
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: prompt,
      },
    ]);

    // Clear input immediately
    setText("");
    setLoading(true);
    setIsThinking(true);

    try {
      const token = localStorage.getItem("token");

      const response = await api.post(
        "/chat",
        {
          session_id: currentSession,
          message: prompt,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // First message -> backend creates session
      if (currentSession === null && response.data.session_id) {
        setCurrentSession(response.data.session_id);
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.data.response,
          tool: response.data.tool,
        },
      ]);
      setIsThinking(false);
    } catch (error) {
      setIsThinking(false);
      console.error(error);

      alert(
        error.response?.data?.detail ||
          error.response?.data ||
          error.message
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="input-box">
      <input
        type="text"
        placeholder="Message ChatGPT..."
        value={text}
        disabled={loading}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
          }
        }}
      />

      <button
        onClick={sendMessage}
        disabled={loading}
      >
        {loading ? "..." : "➤"}
      </button>
    </div>
  );
}

export default InputBox;