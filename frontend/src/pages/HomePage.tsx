import axios from "axios";
import React, { useState, useEffect, useContext } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";

import chat_background from "../assets/wallpaper-universe.jpg";

import "../styling/HomePage.scss";
// import { SlArrowRight } from "react-icons/sl";
import { RiSendPlane2Fill } from "react-icons/ri";

import { AuthContext } from "../context/AuthContext";

interface UsersType {
  users: number;
  username: string;
  avatar: string;
  email: string;
}

interface SelectedUser {
  username: string;
  avatar: string;
}

interface MessageType {
  content: string;
  conversation: string;
  from_user: {
    username: string;
  };
  id: string;
  read: boolean;
  timestamp: string;
  to_user: {
    username: string;
  };
}

const HomePage: React.FC = () => {
  const [usersList, setUsersList] = useState<UsersType[]>();
  const [selectedUser, setSelectedUser] = useState<SelectedUser>();
  const [message, setMessage] = useState<string>("");
  const [messageHistory, setMessageHistory] = useState<MessageType[]>([]);
  const [welcomeMessage, setWelcomeMessage] = useState<string>("");

  const { authTokens } = useContext(AuthContext);

  useEffect(() => {
    const handleSubmit = async () => {
      try {
        const response = await axios.get("http://0.0.0.0:8000/users/");

        console.log("Success:", response.data);
        setUsersList(response.data);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    handleSubmit();
  }, []);

  const handleChatConnection = (user: UsersType) => {
    setSelectedUser(user);
  };

  const send_message = () => {
    const messageData = {
      type: "chat_message",
      message: message,
    };
    sendJsonMessage(messageData);
    setMessage("");
  };

  const { readyState, sendJsonMessage } = useWebSocket(
    selectedUser ? `ws://0.0.0.0:8000/user/${selectedUser.username}/` : "",
    {
      queryParams: {
        token: authTokens ? authTokens.access : "",
      },
      onOpen: () => {
        console.log("Connected!");
      },
      onClose: () => {
        console.log("Disconnected!");
      },

      onMessage: (e) => {
        const data = JSON.parse(e.data);
        console.log(data);
        switch (data.type) {
          case "welcome_message":
            setWelcomeMessage(data.message);
            break;
          case "chat_message_echo":
            setMessageHistory((prev: any) => prev.concat(data.message));
            break;
          case "greeting_reply":
            console.log(data);
            break;
          case "last_50_messages":
            if (data.messages) {
              setMessageHistory(data.messages);
            }
            break;
          default:
            console.log("Unknown message type!");
            console.log(data);
            break;
        }
      },
    }
  );

  const connectionStatus = {
    [ReadyState.CONNECTING]: "Connecting",
    [ReadyState.OPEN]: "Open",
    [ReadyState.CLOSING]: "Closing",
    [ReadyState.CLOSED]: "Closed",
    [ReadyState.UNINSTANTIATED]: "Uninstantiated",
  }[readyState];

  useEffect(() => {
    console.log("Welcome Message: ", welcomeMessage);

    console.log("Selected User: ", selectedUser);

    console.log("Connection Status: ", connectionStatus);
  }, [welcomeMessage, connectionStatus, selectedUser]);

  return (
    <div className="chat-home">
      <div className="sidebar">
        {usersList?.map((user, index) => (
          <div
            key={index}
            className={`user ${
              selectedUser?.username == user.username ? "selected" : ""
            }`}
            onClick={() => handleChatConnection(user)}
          >
            <img src={`http://0.0.0.0:8000${user.avatar}`} alt="User" />
            <span>{user.username}</span>
          </div>
        ))}
      </div>
      <div className="chat-area">
        <img
          className="chat-area_bg"
          src={chat_background}
          alt="Chat Background"
        />

        {selectedUser ? (
          <div className="chat_user-container">
            <div className="chat_reciever-username">
              <img
                src={`http://0.0.0.0:8000${selectedUser.avatar}`}
                alt="reciever profile"
              />
              <div className="chat_user-profile_info">
                <p>{selectedUser.username}</p>
                <span>last seen recently</span>
              </div>
            </div>
            <div className="chat_messageHistory">
              {messageHistory.map((item) => (
                <div className="message_history-box" key={item.id}>
                  <p>{item.from_user.username} :</p>
                  <p>{item.content}</p>
                </div>
              ))}
            </div>
            <div className="chat-area_msg">
              <input
                type="text"
                placeholder="Message"
                onChange={(e) => setMessage(e.target.value)}
              />
              <button onClick={() => send_message()}>
                <RiSendPlane2Fill />
              </button>
            </div>
          </div>
        ) : (
          ""
        )}
      </div>
    </div>
  );
};

export default HomePage;
