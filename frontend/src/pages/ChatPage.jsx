import { useEffect, useRef, useState } from "react";
import { getConversationsByUser, sendChatMessage } from "../api/conversations";
import { jwtDecode } from "jwt-decode";

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  // Decode user info from token (if needed for client-side logic)
  const token = localStorage.getItem("accessToken");
  const userId = token ? jwtDecode(token).user_id : null;

  useEffect(() => {
    fetchConversations();
    inputRef.current?.focus();
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await getConversationsByUser(userId); // No userId passed here
      setMessages(res.data || []);
    } catch (error) {
      console.error("Failed to fetch conversations:", error);
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMsg = { message: trimmed, direction: "user" };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendChatMessage({ message: trimmed }); // No userId in payload
      const botMsg = {
        message: res.data.message,
        direction: "llm",
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className="max-w-2xl mx-auto p-4 h-screen flex flex-col">
      <h1 className="text-2xl font-bold mb-4 text-center">Chat with AI</h1>

      <div className="flex-1 overflow-y-auto bg-gray-100 p-4 rounded shadow-inner">
        {messages.length === 0 && (
          <p className="text-center text-gray-500">Start a conversation…</p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`mb-2 p-3 rounded-lg max-w-[75%] ${
              msg.direction === "user"
                ? "bg-blue-500 text-white ml-auto"
                : "bg-gray-300 text-black"
            }`}
          >
            {msg.message}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="flex items-center mt-4">
        <input
          ref={inputRef}
          type="text"
          className="flex-1 border p-2 rounded-l focus:outline-none"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded-r disabled:opacity-50"
          onClick={handleSend}
          disabled={loading}
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default ChatPage;
