import InputBox from "./InputBox";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { Copy, RotateCcw, ThumbsUp, ThumbsDown } from "lucide-react";

function ChatWindow({
  currentSession,
  setCurrentSession,
  messages,
  setMessages,
  isThinking,
  setIsThinking,
}) {

  const [thinkingText, setThinkingText] = useState("Thinking");

useEffect(() => {
  if (!isThinking) return;

  const frames = [
    "Thinking.",
    "Thinking..",
    "Thinking..."
  ];

  let index = 0;

  const interval = setInterval(() => {
    index = (index + 1) % frames.length;
    setThinkingText(frames[index]);
  }, 400);

  return () => clearInterval(interval);

}, [isThinking]);

  // Copy
  const copyMessage = async (text) => {
    await navigator.clipboard.writeText(text);
    alert("Copied!");
  };

  // Feedback
  const handleFeedback = (messageIndex, type) => {
    console.log("Message:", messageIndex);
    console.log("Feedback:", type);

    alert(type === "like" ? "👍 Thanks for your feedback!" : "👎 Feedback received!");

    // Next step:
    // fetch("/feedback",{...})
  };

  // Retry
  const retryMessage = (assistantIndex) => {
  const userMessage = messages[assistantIndex - 1];

    if (!userMessage) return;

    console.log("Retry Prompt:", userMessage.content);
  };

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

            <div
              key={index}
              className={`message ${msg.role === "user" ? "user-message" : "assistant-message"}`}
            > 
            <div className="message-content">
             {msg.tool && (
  <div className="tool-badge">

    {msg.tool === "web_search" && (
      <>
        🌐 <span>Searching Web</span>
      </>
    )}

    {msg.tool === "weather" && (
      <>
        🌦️ <span>Weather Tool</span>
      </>
    )}

    {msg.tool === "calculator" && (
      <>
        🧮 <span>Calculator Tool</span>
      </>
    )}

    {msg.tool === "memory" && (
      <>
        🧠 <span>Memory Tool</span>
      </>
    )}

    {msg.tool === "llm" && (
      <>
        🤖 <span>AI Knowledge</span>
      </>
    )}

  </div>
)}

              <ReactMarkdown>
                {msg.content}
              </ReactMarkdown>
             </div>

              {msg.role === "assistant" && (

                <div className="message-actions">

                  <button
                    onClick={() => handleFeedback(index, "like")}
                    title="Like"
                  >
                    <ThumbsUp size={17} />
                  </button>

                  <button
                    onClick={() => handleFeedback(index, "dislike")}
                    title="Dislike"
                  >
                    <ThumbsDown size={17} />
                  </button>

                  <button
                    onClick={() => copyMessage(msg.content)}
                    title="Copy"
                  >
                    <Copy size={17} />
                  </button>

                  <button
                    onClick={() => retryMessage(index)}
                    title="Retry"
                  >
                    <RotateCcw size={17} />
                  </button>

                </div>

              )}

            </div>

          ))

        )}
        {isThinking && (
           <div className="assistant-message thinking">

    <div className="thinking-container">

      <div className="thinking-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>

      <p>{thinkingText}</p>

    </div>

  </div>
)}

      </div>

      <InputBox
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

export default ChatWindow;