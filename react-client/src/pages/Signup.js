import axios from "axios";
import React, { useState } from "react";

const url = "http://localhost:5000/";

function Signup() {
  const [userid, setUserid] = useState();
  const [name, setName] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();

  const signupHandler = async (e) => {
    e.preventDefault();

    axios
      .post(url + "flask/signup", {
        userid: userid,
        name: name,
        email: email,
        password: password,
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="login-wrapper">
      <h1>Create a new account</h1>
      <form>
        <label>
          <p>UserID</p>
          <input
            type="text"
            onChange={(e) => {
              setUserid(e.target.value);
            }}
          />
        </label>
        <label>
          <p>Name</p>
          <input
            type="text"
            onChange={(e) => {
              setName(e.target.value);
            }}
          />
        </label>
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
          <button onClick={signupHandler} type="submit">
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}
export default Signup;
