import React, { useState, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styling/HomePage.css";
import { AuthContext } from "../context/AuthContext";

const HomePage: React.FC = () => {
  const [roomName, setRoomName] = useState<string>("");
  const { authTokens } = useContext(AuthContext);

  const navigate = useNavigate();

  return (
    <div className="homepage_container">
      <nav className="homepage_nav">
        <Link to="/">Home</Link>
        <Link to="/login">Login</Link>
        <Link to="/chat">Contact</Link>
      </nav>

      <div className="homepage_hr">
        <hr />
      </div>
    </div>
  );
};

export default HomePage;
