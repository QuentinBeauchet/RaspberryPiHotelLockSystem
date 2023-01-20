const express = require("express");
var cors = require("cors");
const mariadb = require("mariadb");
var bodyParser = require("body-parser");
var app = express();

const port = process.env.PORT;

const doors = {
  1: false,
  2: false,
  3: false,
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

app.get("/api/open", (req, res) => {
  const door = doors[req.query.door_id];
  if (door == undefined) {
    res.sendStatus(404);
    return;
  }
  doors[req.query.door] = true;
  res.send("<h1>Door is Open</h1>");
});

app.get("/api/status", (req, res) => {
  const door = doors[req.query.door];
  if (door == undefined) {
    res.sendStatus(404);
    return;
  }
  res.send({ status: door });
  doors[req.query.door] = false;
});

app.get("/api/user", (req, res) => {
  pool.getConnection().then((conn) => {
    conn
      .query(
        req.query.door_id != undefined
          ? `SELECT DISTINCT users.*
      FROM users
      JOIN \`user permissions\` ON users.rfid = \`user permissions\`.\`user rfid\`
      JOIN \`door permissions\`
      JOIN doors
      WHERE users.rfid = '${req.query.rfid}' AND \`door permissions\`.\`door id\` = '${req.query.door_id}' AND \`user permissions\`.\`permission id\` = \`door permissions\`.\`permission id\`;`
          : `SELECT *
       FROM users
       WHERE users.rfid = '${req.query.rfid}'`
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
  pool.getConnection().then((conn) => {
    conn
      .query(
        `INSERT INTO \`users\` ( \`rfid\`,\`first name\`, \`last name\`, \`picture\`) VALUES
        ('${req.body.rfid}', '${req.body["first name"]}',  '${req.body["last name"]}',  0x${req.body.picture});`
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

app.get("/api/admins", (req, res) => {
  pool.getConnection().then((conn) => {
    conn
      .query(
        `SELECT users.rfid
        FROM users
        JOIN \`user permissions\` ON users.rfid = \`user permissions\`.\`user rfid\`
        JOIN permissions ON \`user permissions\`.\`permission id\` = permissions.id
        WHERE permissions.type = "ADMIN";`
      )
      .then((rows) => {
        res.send(rows);
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
