import React, { useEffect, useState } from "react";
import axios from "axios";
import { Card, Button, Row } from "react-bootstrap";

const url = "http://localhost:5000/";

function Question(props) {
  const [getMessage, setGetMessage] = useState({});
  const [qData, setQData] = useState([]);
  const [aData, setAData] = useState([]);

  useEffect(() => {
    console.log(props.match.params.id);
    axios
      .get(url + "flask/question/" + props.match.params.id)
      .then((response) => {
        setQData(response.data.question_data[0]);
        setAData(response.data.answer_data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  return (
    <div className="App">
      <Card className="m-2">
        <Row>
          <Card.Body className="col-11">
            <Card.Title>{qData[1]}</Card.Title>
            <Card.Text>{qData[2]}</Card.Text>
            <Card.Text>Author: {qData[3]}</Card.Text>
          </Card.Body>
          <div className="col-1">{qData[4]}</div>
        </Row>
      </Card>

      {aData.map((value, index) => {
        return (
          <Card key={index} className="m-2">
            <Card.Body>
              <Row>
                <Card.Body className="col-11">
                  <Card.Text>{value[1]}</Card.Text>
                  <Card.Text>Author: {value[3]}</Card.Text>
                </Card.Body>
                <div className="col-1">{value[4]}</div>
              </Row>
            </Card.Body>
          </Card>
        );
      })}
    </div>
  );
}

export default Question;
