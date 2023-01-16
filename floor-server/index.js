const express = require("express");
var cors = require("cors");
const mariadb = require("mariadb");
var bodyParser = require("body-parser");
var app = express();

const port = process.env.PORT;

const doors = {
  1: "http://localhost:3010",
  2: "http://localhost:3011",
  3: "http://localhost:3012",
};

app.use(bodyParser.json());

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
  pool.getConnection().then((conn) => {
    conn
      .query(
        `SELECT DISTINCT users.*
      FROM users
      JOIN \`user permissions\` ON users.rfid = \`user permissions\`.\`user rfid\`
      JOIN \`door permissions\`
      JOIN doors
      WHERE users.rfid = '${req.query.rfid}' AND \`door permissions\`.\`door id\` = '${req.query.door_id}' AND \`user permissions\`.\`permission id\` = \`door permissions\`.\`permission id\`;`
      )
      .then((rows) => {
        rows.length ? res.send(rows[0]) : res.sendStatus(404);
        conn.end();
      })
      .catch((err) => {
        console.log(err);
        conn.end();
      });
  });
});

app.post("/api/user/add", (req, res) => {
  buf = Buffer.from(req.body.picture).toString("base64");
  pool.getConnection().then((conn) => {
    conn
      .query(
        `INSERT INTO \`users\` ( \`rfid\`,\`first name\`, \`last name\`, \`picture\`) VALUES
        ('${req.body.rfid}', '${req.body["first name"]}',  '${req.body["last name"]}',  '${buf}');`
      )
      .then(() => {
        res.sendStatus(200);
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
