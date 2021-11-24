const { default: axios } = require("axios");
const url = "http://localhost:5000/";
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

  console.time("add_question");
  await axios
    .post(url + "flask/add_question", {
      token,
      title: title + Math.random().toString(),
      desc,
    })
    .then(() => {})
    .catch((error) => {
      console.log(error);
    });
  console.timeEnd("add_question");
}

main();
