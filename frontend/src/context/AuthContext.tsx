import React, { useState, createContext } from "react";
import { AccessTokensInterface } from "../interface/CommonInterface";

interface CurrentUserContextType {
  authTokens: AccessTokensInterface;
  setAuthTokens: React.Dispatch<React.SetStateAction<AccessTokensInterface>>;
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

  return (
    <AuthContext.Provider value={{ authTokens, setAuthTokens }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
