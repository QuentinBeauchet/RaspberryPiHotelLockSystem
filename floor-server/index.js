const express = require("express");
var cors = require("cors");
const mariadb = require("mariadb");
var app = express();

const port = process.env.PORT;

const doors = {
  1: "http://localhost:3010",
  2: "http://localhost:3011",
  3: "http://localhost:3012",
};

app.use(cors());

const pool = mariadb.createPool({
  host: "127.0.0.1",
  user: "root",
  password: "root",
  port: 3306,
  database: "floor",
  connectionLimit: 5,
});

app.get("/api/update", (req, res) => {
  const door = doors[req.query.door];
  if (!door || !["open", "close"].includes(req.query.status)) {
    res.sendStatus(404);
    return;
  }
  res.send(`<h1>Floor: ${process.env.FLOOR}<h1><h2>Door: ${req.query.door}</h2><h3>Status: ${req.query.status}</h3>`);
});

app.get("/api/user", (req, res) => {
  const pool = mariadb.createPool({
    host: "127.0.0.1",
    user: "root",
    password: "root",
    port: 3306,
    database: "floor",
    connectionLimit: 5,
  });

  pool.getConnection().then((conn) => {
    conn
      .query(`SELECT * FROM \`users\` WHERE rfid="${req.query.rfid}"`)
      .then((rows) => {
        if (!rows.length) {
          res.sendStatus(404);
        }
        res.send(rows[0]);
        conn.end();
      })
      .catch((err) => {
        console.log(err);
        conn.end();
      });
  });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
