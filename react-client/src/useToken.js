import { useState } from "react";

export default function useToken() {
  const getToken = (target) => {
    const tokenString = localStorage.getItem(target);
    const userToken = JSON.parse(tokenString);
    if (userToken === null) {
      return null;
    } else {
      console.log("TOKEN LOADED SUCCESSFULLY!");
      return userToken;
    }
  };

  const [token, setToken] = useState(getToken("token"));
  const [userid, setUserid] = useState(getToken("userid"));
  const [name, setName] = useState(getToken("name"));

  const saveToken = (userToken, userid, name) => {
    localStorage.setItem("token", JSON.stringify(userToken));
    localStorage.setItem("userid", JSON.stringify(userid));
    localStorage.setItem("name", JSON.stringify(name));
    setToken(userToken.token);
    setUserid(userid);
    setName(name);
    console.log("TOKEN STORED SUCCESSFULLY!");
  };

  return {
    setToken: saveToken,
    token,
    userid,
    name,
  };
}
