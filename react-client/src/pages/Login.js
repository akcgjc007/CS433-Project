import axios from "axios";
import React, { useState } from "react";
import PropTypes from "prop-types";

import { Button } from "react-bootstrap";
import history from "../history";

const url = "http://localhost:5000/";

function Login({ setToken, setUserInfo }) {
  const [email, setEmail] = useState("a@iitgn.ac.in");
  const [password, setPassword] = useState("abcd");

  const loginHandler = async (e) => {
    e.preventDefault();

    await axios
      .post(url + "flask/login", {
        email: email,
        password: password,
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
