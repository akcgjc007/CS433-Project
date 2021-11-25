import React, { useEffect, useState } from "react";
import axios from "axios";
import { Card, Button, Row, Form } from "react-bootstrap";
import useToken from "../useToken";
import history from "../history";

const url = "http://localhost:5000/";

function Question(props) {
  const [qData, setQData] = useState([]);
  const [aData, setAData] = useState([]);
  const [desc, setDesc] = useState();
  const { token, name, userid } = useToken();

  useEffect(() => {
    console.log(props.match.params.id);
    axios
      .get(url + "flask/question/" + props.match.params.id)
      .then((response) => {
        setQData(response.data.question_data[0]);
        setAData(response.data.answer_data);
        console.log(response.data.answer_data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const addAnswerHandler = async (e) => {
    e.preventDefault();

    await axios
      .post(url + "flask/add_answer", {
        token,
        desc,
        qid: props.match.params.id,
      })
      .then(async (response) => {
        console.log(response);
        history.go(0);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const deleteQuestionHandler = async (e) => {
    e.preventDefault();

    await axios
      .post(url + "flask/delete_question", {
        token,
        qid: props.match.params.id,
      })
      .then(async (response) => {
        console.log(response);
        history.push("/home");
        history.go(0);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const deleteAnswerHandler = async (aid) => {
    await axios
      .post(url + "flask/delete_answer", {
        token,
        aid,
      })
      .then(async (response) => {
        console.log(response);
        history.go(0);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const upvoteQuestionHandler = async (e) => {
    e.preventDefault();

    await axios
      .post(url + "flask/upvote_question", {
        token,
        qid: props.match.params.id,
      })
      .then(async (response) => {
        console.log(response);
        history.go(0);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const upvoteAnswerHandler = async (aid) => {
    await axios
      .post(url + "flask/upvote_answer", {
        token,
        aid,
      })
      .then(async (response) => {
        console.log(response);
        history.go(0);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="App">
      <Card className="m-2">
        <Row>
          <Card.Body className="col-11">
            <Card.Title>
              <h2>{qData[1]}</h2>
            </Card.Title>
            <Card.Text>{qData[2]}</Card.Text>
            <Card.Text>Author: {qData[3]}</Card.Text>
            <Row className="justify-content-center">
              <Button className="mx-2" onClick={upvoteQuestionHandler}>
                Upvote
              </Button>
              <Button className="mx-2">Edit</Button>
              <Button className="mx-2" onClick={deleteQuestionHandler}>
                Delete
              </Button>
            </Row>
          </Card.Body>

          <div className="col-1 border d-flex align-items-center justify-content-center">
            <h3>
              <b>{qData[4]}</b>
            </h3>
          </div>
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
                  <Row className="justify-content-center">
                    <Button
                      className="mx-2"
                      onClick={() => {
                        upvoteAnswerHandler(value[0]);
                      }}
                    >
                      Upvote
                    </Button>
                    <Button className="mx-2">Edit</Button>
                    <Button
                      className="mx-2"
                      onClick={() => {
                        deleteAnswerHandler(value[0]);
                      }}
                    >
                      Delete
                    </Button>
                  </Row>
                </Card.Body>
                <div className="col-1">{value[4]}</div>
              </Row>
            </Card.Body>
          </Card>
        );
      })}

      <br />
      <br />
      <br />

      <Form onSubmit={addAnswerHandler}>
        <Form.Group className="mb-3">
          <Form.Label>
            <h3>Explain your solution</h3>
          </Form.Label>
          <Form.Control
            as="textarea"
            rows={5}
            placeholder="Start writing your solution..."
            onChange={({ target: { value } }) => setDesc(value)}
          />
          <Button type="submit">Answer this question</Button>
        </Form.Group>
      </Form>
    </div>
  );
}

export default Question;
