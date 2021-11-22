import React, { useEffect, useState } from "react";
import axios from "axios";

const url = "http://localhost:5000/";

function Home() {
  const [getMessage, setGetMessage] = useState({});

  useEffect(() => {
    // axios
    //   .get("localhost/flask/hello")
    //   .then((response) => {
    //     console.log("SUCCESS", response);
    //     setGetMessage(response);
    //   })
    //   .catch((error) => {
    //     console.log(error);
    //   });

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
      .get(url + "flask/top_questions")
      .then((response) => {
        console.log("SUCCESS", response);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img className="App-logo" alt="logo" />
        <p>React + Flask Tutorial</p>
        <div>
          {getMessage.status === 200 ? (
            <h3>{getMessage.data.message}</h3>
          ) : (
            <h3>LOADING</h3>
          )}
        </div>
      </header>
    </div>
  );
}

export default Home;
