import React, { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styling/HomePage.css";
import { AuthContext } from "../context/AuthContext";

const HomePage: React.FC = () => {
  const [roomName, setRoomName] = useState<string>("");
  const { authTokens } = useContext(AuthContext);

  const navigate = useNavigate();

  const navigateToRoom = () => {
    authTokens ? navigate(`/chat/${roomName}/`) : "";
  };

  return (
    <div className="homepage_container">
      <h1>Welcome to HomePage</h1>

      <nav className="homepage_nav">
        <Link to="/">Home</Link>
        <Link to="/login">Login</Link>
        <Link to="/chat">Contact</Link>
      </nav>

      <div className="homepage_hr">
        <hr />
      </div>

      <div className="homepage_room-name">
        <input
          type="text"
          name="room"
          placeholder="Enter the room name"
          value={roomName}
          onChange={(e) => setRoomName(e.target.value)}
        />

        {/*How to dynammicaly define the name of the the room */}
        {/* 1. react router for custom url */}
        {/* 2. After redirecting to chat, backend should able to get the room name parameter */}
        <button onClick={() => navigateToRoom()}>Join</button>
      </div>
    </div>
  );
};

export default HomePage;
