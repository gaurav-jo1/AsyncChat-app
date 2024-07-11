import React, { useState, useEffect, useContext, useRef, FormEvent } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import axios from "axios";

import chat_background from "../assets/wallpaper-universe.jpg";

import { RiSendPlane2Fill } from "react-icons/ri";

import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

import "../styling/HomePage.scss";

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
  const [userOnline, setUserOnline] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");
  const [messageHistory, setMessageHistory] = useState<MessageType[]>([]);

  const { authTokens } = useContext(AuthContext);

  const messageContainerRef = useRef<HTMLDivElement | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    const handleSubmit = async () => {
      try {
        const response = await axios.get("http://0.0.0.0:8000/users/", {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + String(authTokens.access),
          },
        });

        console.log("Success:", response.data);
        setUsersList(response.data);
      } catch (error) {
        navigate("/login");
        console.error("Error:", error);
      }
    };

    handleSubmit();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (messageContainerRef.current) {
      messageContainerRef.current.scrollTop =
        messageContainerRef.current.scrollHeight;
    }
  }, [messageHistory]);

  const handleChatConnection = (user: UsersType) => {
    setSelectedUser(user);
  };

  const send_message = (e: FormEvent) => {
    e.preventDefault();
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
        switch (data.type) {
          case "welcome_message":
            break;
          case "chat_message_echo":
            setMessageHistory((prev: MessageType[]) =>
              prev.concat(data.message)
            );
            break;
          case "last_50_messages":
            if (data.messages) {
              setMessageHistory(data.messages);
            }
            break;

          case "user_online_status":
            setUserOnline(false);
            for (let i = 0; i < data.users.length; i++) {
              if (data.users[i].username === selectedUser?.username) {
                setUserOnline(true);
                break; // Exit the loop once a match is found
              }
            }

            break;
          default:
            console.log("Unknown message type!", data);
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
    console.log("Connection Status: ", connectionStatus);
  }, [connectionStatus, userOnline]);

  function convertToReadableTime(timestamp: string): string {
    // Parse the timestamp string into a Date object
    const date = new Date(timestamp);

    // Extract hours and minutes
    let hours = date.getUTCHours();
    const minutes = date.getUTCMinutes();
    
    // Determine AM or PM
    const ampm = hours >= 12 ? 'PM' : 'AM';

    // Convert hours from 24-hour format to 12-hour format
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'

    // Format minutes to always be two digits
    const minutesStr = minutes < 10 ? '0' + minutes : minutes.toString();

    // Combine hours, minutes, and AM/PM into the final string
    const readableTime = `${hours}:${minutesStr} ${ampm}`;

    return readableTime;
}


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
                className={userOnline ? "chat_userprofile-pic" : ""}
                src={`http://0.0.0.0:8000${selectedUser.avatar}`}
                alt="reciever profile"
              />
              <div className="chat_user-profile_info">
                <p>{selectedUser.username}</p>
                {userOnline ? (
                  <span className="chat_user-online">Online</span>
                ) : (
                  <span className="chat_user-offline">last seen recently</span>
                )}
              </div>
            </div>
            <div className="chat_messageHistory" ref={messageContainerRef}>
              {messageHistory.map((item) => (
                <div className="message_history-box" key={item.id}>
                  {item.from_user.username != selectedUser.username ? (
                    <div className="message_history-content_my">
                      <p>{item.content}</p>
                      <span>{convertToReadableTime(item.timestamp)}</span>
                    </div>
                  ) : (
                    ""
                  )}
                  {item.from_user.username == selectedUser.username ? (
                    <div className="message_history-content_from">
                      <p>{item.content}</p>
                      <span>{convertToReadableTime(item.timestamp)}</span>
                    </div>
                  ) : (
                    ""
                  )}
                </div>
              ))}
            </div>
            <form onSubmit={(e) => send_message(e)}  className="chat-area_msg">
              <input
                type="text"
                placeholder="Message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
              />
              <button type="submit">
                <RiSendPlane2Fill />
              </button>
            </form>
          </div>
        ) : (
          ""
        )}
      </div>
    </div>
  );
};

export default HomePage;
