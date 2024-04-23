import React from "react";
import { Link } from "react-router-dom";

const HomePage: React.FC = () => {
  return (
    <div>
      <h1>Welcome to HomePage</h1>

      <nav>
        <Link to="/">Home</Link>
        <Link to="/login">Login</Link>
        <Link to="/chat">Contact</Link>
      </nav>
    </div>
  );
};

export default HomePage;
