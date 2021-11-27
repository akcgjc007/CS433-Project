# CS 433 Project: MINIStackoverflow

## How to run?

### Setting up the server

1. Make sure you have `python`, `mysql` and `mysql-connector` installed in your Ubuntu system.
2. Create a database `mydb` with password `0000`.
3. Run `cd flask-server` to enter the server directory.
4. Run `make schema` to create the schema in the database.
5. Run `make demo` to create some demo entries in the database.
6. Run `flask run` to start the server at `localhost:5000`.

### Starting the client

1. Make sure you have `nodejs` installed in your system.
2. Run `cd python-client` to enter the client directory.
3. `yarn`/`npm i`
4. `yarn start`/`npm run start`

## Testing with `test-client` in `mininet`

- xterm -fa 'Monospace' -fs 14

## References

- [Reine0017/reactFlaskTutorial](https://github.com/Reine0017/reactFlaskTutorial)
- [akcgjc007/IITGN-Grad-Planner](https://github.com/akcgjc007/IITGN-Grad-Planner)
