import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import useToken from "../useToken";
import axios from "axios";
import history from "../history";
import url from "./../url";

export default function AddQuestion() {
  const { token, name, userid } = useToken();
  const [title, setTitle] = useState();
  const [desc, setDesc] = useState();
  const [tags, setTags] = useState();

  const addQuestionHandler = async (e) => {
    e.preventDefault();

    await axios
      .post(url + "flask/add_question", {
        token,
        title,
        desc,
        tags: tags.split(","),
      })
      .then(async (response) => {
        console.log("Response: ", response);
        history.push("/question/" + response.data.qid);
        history.go(0);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div className="login-wrapper p-2">
      <h1>Ask a question</h1>
      <Form onSubmit={addQuestionHandler}>
        <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Start writing your question title..."
            onChange={({ target: { value } }) => setTitle(value)}
          />
          <Form.Label>Explain your question</Form.Label>
          <Form.Control
            as="textarea"
            rows={5}
            placeholder="Start writing your question description..."
            onChange={({ target: { value } }) => setDesc(value)}
          />
          <Form.Label>Write Tags(comma separated)</Form.Label>
          <Form.Control
            as="textarea"
            rows={5}
            placeholder="tag1,tag2,..."
            onChange={({ target: { value } }) => setTags(value)}
          />

          <Button type="submit">Add question</Button>
        </Form.Group>
      </Form>
    </div>
  );
}
