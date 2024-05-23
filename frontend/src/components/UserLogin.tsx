import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

import "../styling/UserLogin.scss"

const UserLogin: React.FC = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [userLogged, setUserLogged] = useState<boolean>(false);
  const { setAuthTokens } = useContext(AuthContext);

  useEffect(() => {
    console.log(userLogged);

    if (userLogged) {
      navigate("/");
    }
  }, [userLogged]);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = {
      username: username,
      password: password,
    };

    try {
      const response = await axios.post(
        "http://0.0.0.0:8000/api/token/",
        formData
      );

      console.log("Success:", response.data);
      setAuthTokens(response.data.tokens);
      setUsername(response.data.username);
      localStorage.setItem("authTokens", JSON.stringify(response.data.tokens));
      localStorage.setItem("username", JSON.stringify(response.data.username));
      setUserLogged(true);
    } catch (error) {
      console.error("Error:", error);
    }
  };


return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
      </form>
    
    </div>
  );
};

export default UserLogin;
