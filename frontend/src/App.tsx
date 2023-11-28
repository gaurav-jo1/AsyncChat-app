import React, { useState, useEffect } from "react";
import "./App.css";

// import axios from "axios";

interface language_list {
  id: string;
  language_name: string;
}

const App: React.FC = () => {
  const [data, setData] = useState<language_list[]>();
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);

  // const [loading, setLoading] = useState(true);
  // const [error, setError] = useState(null);

  // const fetchData = () => {
  //   axios
  //     .get("http://127.0.0.1:8000/api/")
  //     .then((response) => {
  //       // Assuming the response.data contains the data you need
  //       setData(response.data.languages);
  //     })
  //     .catch((error) => {
  //       setError(error);
  //     })
  //     .finally(() => {
  //       setLoading(false);
  //     });
  // };

  const fetchA_Data = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/");

      if (!response.ok) {
        throw new Error("Network request failed");
      }

      const result = await response.json();
      console.log(result);
      setData(result);
    } catch (error) {
      console.log(error);
    } finally {
      console.log(false);
    }
  };

  useEffect(() => {
    // Replace 'ws://localhost:8080' with your WebSocket server URL
    const ws = new WebSocket("ws://localhost:8080");

    ws.onopen = () => {
      console.log("WebSocket connection opened");
    };

    ws.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    setSocket(ws);

    return () => {
      // Clean up the WebSocket connection when the component is unmounted
      ws.close();
    };
  }, []); // The empty dependency array ensures that this effect runs only once

  const sendMessage = () => {
    if (socket) {
      // Replace 'Hello, WebSocket!' with your message
      socket.send("Hello, WebSocket!");
    }
  };

  return (
    <div>
      <h1>Hello World</h1>

      <div>
        <button onClick={() => fetchA_Data()}> Get List of Languages</button>
      </div>

      {data &&
        data.map((item) => (
          <div key={item.id}>
            <p>{item.language_name}</p>
          </div>
        ))}

      {/* WebSocket */}
      <div className="websocket">
        <input type="text" placeholder="Enter text" />
        <input
          type="submit"
          placeholder="Send Message"
          onClick={() => sendMessage()}
        />
      </div>

      <div>
        <ul>
          {messages.map((message, index) => (
            <li key={index}>{message}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;
