import React from "react";
import { Router, Switch, Route } from "react-router-dom";
// import Login from "./pages/Login";
import Home from "./pages/Home";
import NotFound from "./pages/404";
import history from "./history";
import Question from "./pages/Question";

function Routes() {
  return (
    <Router history={history}>
      <Switch>
        <Route path="/home" exact component={Home} />
        <Route path="/question/:id" exact component={Question} />

        {/* <Route path="/login" component={Login} /> */}

        <Route component={NotFound} />
      </Switch>
    </Router>
  );
}

export default Routes;
