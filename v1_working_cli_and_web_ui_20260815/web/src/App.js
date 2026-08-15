import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'ami',
      text: '🔥 ANGRY AMI 🔥\n\nCharlie is DeMan, wetin de matter?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: input,
      timestamp: new Date()
    };
    
    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();

      if (response.ok) {
        const amiMessage = {
          id: messages.length + 2,
          sender: 'ami',
          text: data.ami_response,
          timestamp: new Date()
        };
        setMessages(msgs => [...msgs, amiMessage]);
      } else {
        const errorMessage = {
          id: messages.length + 2,
          sender: 'ami',
          text: 'Sorry, I ran into an error. Let me get back to you.',
          timestamp: new Date()
        };
        setMessages(msgs => [...msgs, errorMessage]);
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: messages.length + 2,
        sender: 'ami',
        text: 'Connection error. Make sure the server is running.',
        timestamp: new Date()
      };
      setMessages(msgs => [...msgs, errorMessage]);
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🔥 ANGRY AMI 🔥</h1>
          <p>Charlie is DeMan's Personal AI Partner</p>
        </div>

        <div className="chat-messages">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.sender}`}>
              <div className="message-bubble">
                <p>{message.text}</p>
                <span className="timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
          {loading && (
            <div className="message ami">
              <div className="message-bubble typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="chat-input-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="You: "
            disabled={loading}
            autoFocus
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
