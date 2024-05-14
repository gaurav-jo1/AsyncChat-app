import React, { useContext, useState } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

// Styling
import "../styling/ChatPage.css";
import { AuthContext } from "../context/AuthContext";

interface MessageType {
  type: string;
  username: string;
  message: string;
}

const ChatPage: React.FC = () => {
  const { roomname } = useParams<{ roomname: string }>();

  const [message, setMessage] = useState<string>("");
  const [messageHistory, setMessageHistory] = useState<MessageType[]>([]);
  const [welcomeMessage, setWelcomeMessage] = useState<string>("");

  const { authTokens } = useContext(AuthContext);

  const navigate = useNavigate();

  const send_message = () => {
    const messageData = {
      type: "chat_message",
      message: message,
    };
    sendJsonMessage(messageData);
    setMessage("");
  };

  const { readyState,sendJsonMessage } = useWebSocket(`ws://0.0.0.0:8000/chat/${roomname}/`, {
    queryParams: {
      token: authTokens ? authTokens.access : "",
    },
    onOpen: () => {
      console.log("Connected!");
    },
    onClose: () => {
      console.log("Disconnected!");
      navigate("/");
    },

    onMessage: (e) => {
      const data = JSON.parse(e.data);
      console.log(data)
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
          console.log(data);
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
        <h1>{roomname}</h1>
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
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter the Message"
        />
        <button onClick={() => send_message()}>Send</button>
      </div>
    </div>
  );
};

export default ChatPage;
