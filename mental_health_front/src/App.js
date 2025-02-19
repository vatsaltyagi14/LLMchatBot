import React, { useState, useEffect, useRef } from 'react';
import './App.css';

function App() {
  const [userId] = useState("demo_user");
  const [mode] = useState("just_chat");
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Fetch existing chat history when the component mounts
  useEffect(() => {
    fetchChatHistory();
  }, []);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory]);

  const fetchChatHistory = async () => {
    try {
      const response = await fetch(`http://localhost:8000/history?user_id=${userId}`);
      const data = await response.json();
      setChatHistory(data);
    } catch (err) {
      console.error("Error fetching chat history:", err);
      setError("Failed to load chat history");
    }
  };

  const sendMessage = async () => {
    if (!message.trim()) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message, mode })
      });
      const data = await response.json();
      // Append the new conversation pair to the chat history
      setChatHistory(prev => [...prev, { user: message, response: data.response }]);
      setMessage("");
    } catch (err) {
      console.error("Error sending message:", err);
      setError("Failed to send message. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // NEW FUNCTION: reset chat history
  const resetChatHistory = async () => {
    try {
      await fetch(`http://localhost:8000/history?user_id=${userId}`, {
        method: "DELETE",
      });
      setChatHistory([]);
    } catch (err) {
      console.error("Error resetting chat history:", err);
      setError("Failed to reset chat history");
    }
  };
  

  // Allow sending with Enter (without Shift) and multi-line editing with Shift+Enter
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-app">
      <header className="chat-header">
        <h1>Mental Health Chatbot</h1>
      </header>

      <div className="chat-window">
        {chatHistory.map((chat, index) => (
          <div key={index} className="chat-pair">
            <div className="chat-bubble user-bubble">
              <span className="bubble-label">You:</span> {chat.user}
            </div>
            <div className="chat-bubble bot-bubble">
              <span className="bubble-label">Bot:</span> {chat.response}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="chat-bubble bot-bubble">
            <span className="bubble-label">Bot:</span> Typing...
          </div>
        )}
        <div ref={messagesEndRef}></div>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="input-area">
        <textarea
          className="message-input"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
        />
        <button className="send-button" onClick={sendMessage} disabled={isLoading}>
          Send
        </button>

        {/* NEW RESET BUTTON */}
        <button className="reset-button" onClick={resetChatHistory} disabled={isLoading}>
          Reset
        </button>
      </div>
    </div>
  );
}

export default App;
