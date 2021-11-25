import axios from "axios";
import React, { useEffect, useState } from "react";
import { Card, Row } from "react-bootstrap";
import history from "../history";
import url from "../url";

export default function UserProfile(props) {
  const [rep, setRep] = useState(0);
  const [postData, setPostData] = useState([]);
  useEffect(() => {
    axios
      .get(url + "flask/user/" + props.match.params.userid)
      .then((response) => {
        setRep(response.data.reputation);
        setPostData(response.data.qData);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <Card className="text-center">
        <Card.Body>
          <Card.Title>UserID: {props.match.params.userid}</Card.Title>
          <Card.Title>
            <h3>User reputation: {rep}</h3>
          </Card.Title>
        </Card.Body>
      </Card>

      <br />

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
