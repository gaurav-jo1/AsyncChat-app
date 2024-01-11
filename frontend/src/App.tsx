import React, { useState, useEffect } from "react";

const App: React.FC = () => {
  const [socket, setSocket] = useState<any>(null);
  const [message, setMessage] = useState<string>("");

  useEffect(() => {
    // Replace 'ws://localhost:8080' with your WebSocket server URL
    const ws = new WebSocket("ws://0.0.0.0:8000/ws/chat/1/");

    console.log("WS", ws)

    ws.addEventListener("open", () => {
      console.log("WebSocket connection established");
    });

    ws.addEventListener("message", (event) => {
      console.log(`Received message: ${event.data}`);
    });

    ws.addEventListener("close", () => {
      console.log("WebSocket connection closed");
    });

    setSocket(ws);
  }, []);

  const sendMessage = () => {
    if (socket) {
      socket.send(message);
    }
  };

  return (
    <div>
      <textarea cols={100} rows={20}></textarea> <br />
      <input
        type="text"
        placeholder="Enter message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <input type="submit" onClick={sendMessage} />
    </div>
  );
};

export default App;
