import React from "react";
import HomePage from "./pages/HomePage";
import UserLogin from "./pages/UserLogin";
import ChatPage from "./pages/ChatPage";

import AuthProvider from "./context/AuthContext";
import { ProtectedRoutes } from "./secure_routes/ProtectedRoutes";

import { Navigate, Route, Routes } from "react-router-dom";

const App: React.FC = () => {
  return (
    <div>
      <AuthProvider>
        <Routes>
          <Route path="*" element={<Navigate to="/" replace />} />
          {/* <Route path="/" element={<HomePage />} /> */}
          <Route path="/login" element={<UserLogin />} />
          <Route
            path="/"
            element={
              <ProtectedRoutes>
                <HomePage />
              </ProtectedRoutes>
            }
          />
          {/* <Route
            path="/chat/:roomname"
            element={
              <ProtectedRoutes>
                <ChatPage />
              </ProtectedRoutes>
            }
          /> */}
        </Routes>
      </AuthProvider>
    </div>
  );
};

export default App;
