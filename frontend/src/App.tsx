import React from "react";
import HomePage from "./components/HomePage";
import UserLogin from "./components/UserLogin";
import ChatPage from "./components/ChatPage";

import AuthProvider from "./context/AuthContext";

import { Navigate, Route, Routes } from "react-router-dom";

const App: React.FC = () => {
  return (
    <div>
      <AuthProvider>
        <Routes>
          <Route path="*" element={<Navigate to="/" replace />} />
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<UserLogin />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </AuthProvider>
    </div>
  );
};

export default App;
