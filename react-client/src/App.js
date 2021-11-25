import React, { useState } from "react";
import Navigation from "./comp/Navbar";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import "./App.css";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Home from "./pages/Home";
import Question from "./pages/Question";
import { Row } from "react-bootstrap";
import useToken from "./useToken";
import AddQuestion from "./pages/AddQuestion";
import TagSearch from "./pages/TagSearch";

function App() {
  const { token, setToken } = useToken();
  if (!token) {
    return (
      <Row>
        <link
          rel="stylesheet"
          href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
        />
        <div className="col-6">
          <Login setToken={setToken} />
        </div>
        <div className="col-6">
          <Signup />
        </div>
      </Row>
    );
  }

  return (
    <div>
      <link
        rel="stylesheet"
        href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
      />
      <Navigation />
      <BrowserRouter>
        <Switch>
          <Route path="/home" component={Home} />
          <Route path="/question/:id" component={Question} />
          <Route path="/add_question" component={AddQuestion} />
          <Route path="/tag_search/:name" component={TagSearch} />
        </Switch>
      </BrowserRouter>
    </div>
  );
}

export default App;
