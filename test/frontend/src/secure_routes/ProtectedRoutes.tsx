import { useContext } from "react";
import { Navigate } from "react-router-dom";

import { AuthContext } from "../context/AuthContext";

export const ProtectedRoutes = ({ children }: { children: any }) => {
  const { authTokens } = useContext(AuthContext);

  if (!authTokens) {
    return <Navigate to="/login" replace />;
  }

  return children;
};
