import axios from "axios";
import React, { useState } from "react";
import PropTypes from "prop-types";
import history from "../history";
import crypto from "crypto";

import url from "./../url";

function hash_base64(password) {
  return crypto.createHash("sha256").update(password).digest("base64");
}

function Login({ setToken }) {
  const [email, setEmail] = useState("a@iitgn.ac.in");
  const [password, setPassword] = useState("abcd");

  const loginHandler = async (e) => {
    e.preventDefault();

    await axios
      .post(url + "flask/login", {
        email: email,
        password: hash_base64(password),
      })
      .then(async (response) => {
        if (response.data.status === "Success") {
          setToken(
            response.data.token,
            response.data.userid,
            response.data.name
          );
          history.push("/home");
          history.go(0);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="login-wrapper">
      <h1>Please Log In</h1>
      <form>
        <label>
          <p>Email</p>
          <input
            type="email"
            onChange={(e) => {
              setEmail(e.target.value);
            }}
          />
        </label>
        <label>
          <p>Password</p>
          <input
            type="password"
            onChange={(e) => {
              setPassword(e.target.value);
            }}
          />
        </label>
        <div>
          <button onClick={loginHandler} type="submit">
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}
Login.propTypes = {
  setToken: PropTypes.func.isRequired,
};
export default Login;
