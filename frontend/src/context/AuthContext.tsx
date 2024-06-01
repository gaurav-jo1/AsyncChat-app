import React, { useState, useEffect, createContext } from "react";
import { AccessTokensInterface } from "../interface/CommonInterface";
import axios from "axios";
import { AxiosResponse, AxiosError } from "axios";

interface CurrentUserContextType {
  authTokens: AccessTokensInterface;
  setAuthTokens: React.Dispatch<React.SetStateAction<AccessTokensInterface>>;
  currentUser: string;
  setCurrentUser: React.Dispatch<React.SetStateAction<string>>;
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

  const [currentUser, setCurrentUser] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  function callLogout() {
    setAuthTokens({ access: undefined, refresh: undefined });
    localStorage.removeItem("authTokens");
  }

  function updateAccess() {
    axios
      .post("http://0.0.0.0:8000/api/token/refresh/", {
        refresh: authTokens.refresh,
      })
      .then((response: AxiosResponse) => {
        setAuthTokens(response.data);
        localStorage.setItem("authTokens", JSON.stringify(response.data));
        setLoading(true);
      })
      .catch((error: AxiosError) => {
        console.log(error);
        callLogout();
        setLoading(true);
      });
  }

  useEffect(() => {
    if (authTokens && !loading) {
      updateAccess();
    }

    if (!authTokens) {
      setLoading(true);
    }

    const twentyMinutes = 1000 * 60 * 20;
    const interval = setInterval(() => {
      if (authTokens) {
        updateAccess();
      }
    }, twentyMinutes);
    return () => clearInterval(interval);
  }, [authTokens, loading]); // eslint-disable-line

  return (
    <AuthContext.Provider
      value={{ authTokens, setAuthTokens, currentUser, setCurrentUser }}
    >
      {loading ? children : null}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
