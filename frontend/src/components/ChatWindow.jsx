import InputBox from "./InputBox";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import {
  Copy,
  RotateCcw,
  ThumbsUp,
  ThumbsDown,
} from "lucide-react";

function ChatWindow({
  currentSession,
  setCurrentSession,
  messages,
  setMessages,
  isThinking,
  setIsThinking,
}) {
  const [thinkingText, setThinkingText] = useState("Thinking");

  // ================================
  // Thinking animation
  // ================================

  useEffect(() => {
    if (!isThinking) return;

    const frames = [
      "Thinking.",
      "Thinking..",
      "Thinking...",
    ];

    let index = 0;

    const interval = setInterval(() => {
      index = (index + 1) % frames.length;
      setThinkingText(frames[index]);
    }, 400);

    return () => clearInterval(interval);
  }, [isThinking]);

  // ================================
  // Copy message
  // ================================

  const copyMessage = async (text) => {
    await navigator.clipboard.writeText(text);
    alert("Copied!");
  };

  // ================================
  // Feedback
  // ================================

  const handleFeedback = (messageIndex, type) => {
    console.log("Message:", messageIndex);
    console.log("Feedback:", type);

    alert(
      type === "like"
        ? "👍 Thanks for your feedback!"
        : "👎 Feedback received!"
    );
  };

  // ================================
  // Retry
  // ================================

  const retryMessage = (assistantIndex) => {
    const userMessage = messages[assistantIndex - 1];

    if (!userMessage) return;

    console.log("Retry Prompt:", userMessage.content);
  };

  // ================================
  // Tool display
  // ================================

  const renderTool = (tool) => {
    switch (tool) {
      case "web_search":
        return "🌐 Searching Web";

      case "weather":
        return "🌦️ Weather Tool";

      case "calculator":
        return "🧮 Calculator Tool";

      case "memory":
        return "🧠 Memory Tool";

      case "time":
        return "🕐 Time Tool";

      case "llm":
        return "🤖 AI Knowledge";

      default:
        return tool;
    }
  };

  // ================================
  // UI
  // ================================

  return (
    <div className="chat-window">

      {/* Navbar */}
      <div className="navbar">
        <h2>ChatGPT Clone</h2>
      </div>

      {/* Messages */}
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
              className={`message ${
                msg.role === "user"
                  ? "user-message"
                  : "assistant-message"
              }`}
            >

              {/* Message Content */}
              <div className="message-content">

                {/* ================================
                    TOOL INFORMATION
                ================================= */}

                {msg.role === "assistant" &&
                  msg.tool &&
                  (
                    Array.isArray(msg.tool)
                      ? msg.tool.length > 0
                      : true
                  ) && (

                    <div className="tools-used">

                      {Array.isArray(msg.tool) ? (

                        msg.tool.map((tool, toolIndex) => (

                          <span
                            key={toolIndex}
                            className="tool-badge"
                          >
                            {renderTool(tool)}
                          </span>

                        ))

                      ) : (

                        <span className="tool-badge">
                          {renderTool(msg.tool)}
                        </span>

                      )}

                    </div>

                  )}

                {/* ================================
                    AI / USER MESSAGE
                ================================= */}

                <ReactMarkdown>
                  {msg.content}
                </ReactMarkdown>

              </div>

              {/* ================================
                  ASSISTANT ACTIONS
              ================================= */}

              {msg.role === "assistant" && (

                <div className="message-actions">

                  <button
                    onClick={() =>
                      handleFeedback(index, "like")
                    }
                    title="Like"
                  >
                    <ThumbsUp size={17} />
                  </button>

                  <button
                    onClick={() =>
                      handleFeedback(index, "dislike")
                    }
                    title="Dislike"
                  >
                    <ThumbsDown size={17} />
                  </button>

                  <button
                    onClick={() =>
                      copyMessage(msg.content)
                    }
                    title="Copy"
                  >
                    <Copy size={17} />
                  </button>

                  <button
                    onClick={() =>
                      retryMessage(index)
                    }
                    title="Retry"
                  >
                    <RotateCcw size={17} />
                  </button>

                </div>

              )}

            </div>

          ))

        )}

        {/* ================================
            THINKING
        ================================= */}

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

      {/* Input */}
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