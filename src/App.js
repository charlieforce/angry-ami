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
  const [uploading, setUploading] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;

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
      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });

      const data = await response.json();

      if (data.ami_response) {
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
          text: data.error || 'Error connecting to Ami.',
          timestamp: new Date()
        };
        setMessages(msgs => [...msgs, errorMessage]);
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: messages.length + 2,
        sender: 'ami',
        text: `Connection error: ${error.message}`,
        timestamp: new Date()
      };
      setMessages(msgs => [...msgs, errorMessage]);
    }

    setLoading(false);
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (data.status === 'success') {
        const amiMessage = {
          id: messages.length + 1,
          sender: 'ami',
          text: `🎉 ${data.message}\n\nI've learned from this document! You can now ask me questions about it.`,
          timestamp: new Date()
        };
        setMessages(msgs => [...msgs, amiMessage]);
      } else {
        const errorMessage = {
          id: messages.length + 1,
          sender: 'ami',
          text: `Error uploading document: ${data.error}`,
          timestamp: new Date()
        };
        setMessages(msgs => [...msgs, errorMessage]);
      }
    } catch (error) {
      console.error('Upload error:', error);
      const errorMessage = {
        id: messages.length + 1,
        sender: 'ami',
        text: `Upload failed: ${error.message}`,
        timestamp: new Date()
      };
      setMessages(msgs => [...msgs, errorMessage]);
    }

    setUploading(false);
    fileInputRef.current.value = '';
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
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept=".txt,.pdf,.docx"
            style={{ display: 'none' }}
          />
          <button
            type="button"
            onClick={() => fileInputRef.current.click()}
            disabled={uploading || loading}
            className="upload-btn"
            title="Upload document (TXT, PDF, DOCX)"
          >
            📎
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Talk to Ami..."
            disabled={loading || uploading}
            autoFocus
          />
          <button type="submit" disabled={loading || uploading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
