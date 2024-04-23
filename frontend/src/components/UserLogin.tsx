import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const UserLogin: React.FC = () => {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [userLogged, setUserLogged] = useState<boolean>(false);
  const { setAuthTokens, setUsername } = useContext(AuthContext);

  useEffect(() => {
    console.log(userLogged);

    if (userLogged) {
      navigate("/chat");
    }
  }, [userLogged]);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = {
      email: email,
      password: password,
    };

    try {
      //   const response = await fetch("http://0.0.0.0:8000/api/token/", {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify(formData),
      //   });

      //   const result = await response.json();
      //   console.log("Success:", result);

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
    <div>
      <h1>Login</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Enter Your Email"
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          name="password"
          placeholder="Enter the Password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Log In</button>
      </form>
    </div>
  );
};

export default UserLogin;
