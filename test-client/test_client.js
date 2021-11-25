const { default: axios } = require("axios");
import url from "./../url";
const { title, desc } = require("./raw_data");

async function main() {
  let token;
  let email = "a@iitgn.ac.in";
  let password = "abcd";
  console.time("login");
  await axios
    .post(url + "flask/login", {
      email,
      password,
    })
    .then(async (response) => {
      if (response.data.status === "Success") {
        token = response.data.token;
      }
    })
    .catch((error) => {
      console.log(error);
    });
  console.timeEnd("login");

  let qArr = [];

  for (let i = 0; i < 5; i++) {
    console.time("add_question" + i);
    await axios
      .post(url + "flask/add_question", {
        token,
        title: title + Math.random().toString(),
        desc,
      })
      .then((response) => {
        qArr.push(response.data.qid);
      })
      .catch((error) => {
        console.log(error);
      });
    console.timeEnd("add_question" + i);
  }

  let aArr = [];
  for (let i = 0; i < 5; i++) {
    console.time("add_answer" + i);
    await axios
      .post(url + "flask/add_answer", {
        token,
        desc,
        qid: qArr[i],
      })
      .then((response) => {
        aArr.push(response.data.aid);
      })
      .catch((error) => {
        console.log(error);
      });
    console.timeEnd("add_answer" + i);
  }

  for (let i = 0; i < 5; i++) {
    console.time("add_answer" + i);
    await axios
      .post(url + "flask/delete_answer", {
        token,
        aid: aArr[i],
      })
      .then(() => {})
      .catch((error) => {
        console.log(error);
      });
    console.timeEnd("add_answer" + i);
  }

  for (let i = 0; i < qArr.length; i++) {
    console.time("delete_question" + i);
    await axios
      .post(url + "flask/delete_question", {
        token,
        qid: qArr[i],
      })
      .then(() => {})
      .catch((error) => {
        console.log(error);
      });
    console.timeEnd("delete_question" + i);
  }
}

main();
