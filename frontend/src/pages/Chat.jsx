import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

function Chat() {
  return (
    <div className="chat-container">
      <Sidebar />
      <ChatWindow />
    </div>
  );
}

export default Chat;