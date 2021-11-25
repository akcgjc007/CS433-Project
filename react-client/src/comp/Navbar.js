import axios from "axios";
import React, { useEffect, useState } from "react";
import {
  Navbar,
  Nav,
  Form,
  FormControl,
  Button,
  Col,
  Popover,
  Row,
  OverlayTrigger,
} from "react-bootstrap";
import history from "../history";
import url from "./../url";

function Navigation(props) {
  const [term, setTerm] = useState();

  return (
    <Navbar className="bg-dark px-2" sticky="top">
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Brand href="/home" style={{ color: "white" }}>
        <strong>MiniStackOverFlow</strong>
      </Navbar.Brand>
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link style={{ color: "white" }} href="/home">
            Home
          </Nav.Link>
          <Nav.Link
            style={{ color: "white" }}
            onClick={() => {
              history.push("/user/" + props.userid);
              history.go(0);
            }}
          >
            Profile
          </Nav.Link>
          <Nav.Link
            onClick={() => {
              localStorage.clear();
              history.go(0);
            }}
            style={{ color: "white" }}
          >
            Logout
          </Nav.Link>
          <Nav.Link href="/add_question">
            <Button className="py-0">Add a question</Button>
          </Nav.Link>
        </Nav>
      </Navbar.Collapse>
      <Form
        inline
        onSubmit={(e) => {
          e.preventDefault();
          history.push("/tag_search/" + term);
          history.go(0);
        }}
      >
        <FormControl
          type="text"
          placeholder="Search..."
          className="mr-4 my-auto"
          onChange={(e) => {
            setTerm(e.target.value);
          }}
        />

        <Button
          variant="outline-light"
          onClick={() => {
            history.push("/tag_search/" + term);
            history.go(0);
          }}
        >
          Go
        </Button>
      </Form>
    </Navbar>
  );
}

export default Navigation;
