import React, { useState, createContext } from "react";
import { AccessTokensInterface } from "../interface/CommonInterface";

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


  // useEffect(() => {

  //   const getUser = async () => {
  //     try {
  //       const response = await axios.get("http://0.0.0.0:8000/users/");

  //       console.log("Success:", response.data);
  //       setCurrentUser(response.data);
  //     } catch (error) {
  //       console.error("Error:", error);
  //     }
  //   }

  // }, [])

  return (
    <AuthContext.Provider value={{ authTokens, setAuthTokens, currentUser, setCurrentUser}}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
