import React, { useContext, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

// Styling
import "../styling/ChatPage.css";
import { AuthContext } from "../context/AuthContext";

interface MessageType {
  type: string;
  username: string;
  message: string
}

const ChatPage: React.FC = () => {
  const [message, setMessage] = useState<string>("");
  const [messageHistory, setMessageHistory] = useState<MessageType[]>([]);
  const [welcomeMessage, setWelcomeMessage] = useState<string>("");
  
  const { username } = useContext(AuthContext);

  const { sendJsonMessage } = useWebSocket(
    "ws://127.0.0.1:8000/chat/game_room/"
  );

  const send_message = () => {
    setMessage("");
    sendJsonMessage({
      type: "message",
      message: message,
      username: username,
    });
  };

  const { readyState } = useWebSocket("ws://127.0.0.1:8000/chat/game_room/", {
    onOpen: () => {
      console.log("Connected!");
    },
    onClose: () => {
      console.log("Disconnected!");
    },

    onMessage: (e) => {
      const data = JSON.parse(e.data);
      switch (data.type) {
        case "welcome_message":
          setWelcomeMessage(data.message);
          break;
        case "message":
          setMessageHistory((prev: any) => prev.concat(data));
          break;
        case "greeting_reply":
          console.log(data);
          break;
        default:
          console.log("Unknown message type!");
          break;
      }
    },
  });

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  return (
    <div className="chatpage_container">
      {/* Main body */}
      <div className="chatpage_main-body">
        <h1>ChatPage</h1>
        <span>The WebSocket is currently {connectionStatus}</span>
        <span>{welcomeMessage}</span>

        <div className="chatpage_button">
          <button
            className="bg-gray-300 px-3 py-1"
            onClick={() => {
              sendJsonMessage({
                type: "greeting",
                message: "Hi!",
              });
            }}
          >
            Say Hi
          </button>
        </div>
      </div>

      <div>
        <hr />
      </div>

      {/* Text Messages */}

      <div className="message_history">
        {messageHistory.map((item, index: number) => (
          <div className="message_history-box" key={index}>
            <p>{item.username} :</p>
            <p>{item.message}</p>
          </div>
        ))}
      </div>

      <div className="chatpage_messages">
        <input
          type="text"
          name="message"
          onChange={(e) => setMessage(e.target.value)}
          value={message}
          placeholder="Enter the Message"
        />
        <button onClick={() => send_message()}>Send</button>
      </div>
    </div>
  );
};

export default ChatPage;
