import React, { useEffect, useState } from "react";
import { Card, Button, Row } from "react-bootstrap";
import history from "./../history";

import axios from "axios";
const url = "http://localhost:5000/";

function Home() {
  const [getMessage, setGetMessage] = useState({});
  const [postData, setPostData] = useState([]);

  useEffect(() => {
    axios
      .get(url + "flask/hello")
      .then((response) => {
        console.log("SUCCESS", response);
        setGetMessage(response);
      })
      .catch((error) => {
        console.log(error);
      });

    axios
      .get(url + "flask/all")
      .then((response) => {
        console.log(response);
        setPostData(response.data.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  return (
    <div className="App">
      {postData.map((value, index) => {
        console.log(value);
        return (
          <Card
            key={index}
            onClick={() => {
              history.push("/question/" + value[0]);
              history.go(0);
            }}
            className="m-2"
          >
            <Card.Body>
              <Row>
                <Card.Title className="col-11">{value[1]}</Card.Title>
                <div className="col-1">{value[4]}</div>
              </Row>
            </Card.Body>
          </Card>
        );
      })}
    </div>
  );
}

export default Home;
