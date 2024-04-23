import React, { useState, createContext } from "react";
import { AccessTokensInterface } from "../interface/CommonInterface";

interface CurrentUserContextType {
  authTokens: AccessTokensInterface;
  setAuthTokens: React.Dispatch<React.SetStateAction<AccessTokensInterface>>;
  username: string;
  setUsername: React.Dispatch<React.SetStateAction<string>>;
}

export const AuthContext = createContext<CurrentUserContextType>(
  {} as CurrentUserContextType
);

interface AuthProviderProps {
  children: React.ReactNode;
}

const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [authTokens, setAuthTokens] = useState<AccessTokensInterface>(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens") || "")
      : undefined
  );

  const [username, setUsername] = useState<string>(() =>
    localStorage.getItem("username")
      ? JSON.parse(localStorage.getItem("username") || "")
      : ""
  );

  return (
    <AuthContext.Provider
      value={{ authTokens, setAuthTokens, username, setUsername }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
