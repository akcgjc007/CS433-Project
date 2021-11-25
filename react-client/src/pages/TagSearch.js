import React, { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";
import history from "../history";
import axios from "axios";

import url from "./../url";
export default function TagSearch(props) {
  const [titleArray, setTitleArray] = useState([]);
  useEffect(() => {
    axios
      .get(url + "flask/tags/" + props.match.params.name)
      .then((response) => {
        console.log(response);
        setTitleArray(response.data.title_array);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  return (
    <div>
      {titleArray.map((value, index) => {
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
                <Card.Title className="col-11 text-center">
                  {value[1]}
                </Card.Title>
              </Row>
            </Card.Body>
          </Card>
        );
      })}
    </div>
  );
}
