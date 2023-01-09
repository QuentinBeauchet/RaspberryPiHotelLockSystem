const express = require("express");
var cors = require("cors");
const fetch = require("node-fetch");
const fs = require("fs");
var app = express();

const port = 3000;

app.use(cors());

const floors = JSON.parse(fs.readFileSync(`../floors.json`));
const doors = JSON.parse(fs.readFileSync(`../doors.json`));

app.get("/api/update", (req, res) => {
  const door = doors[req.query.door];
  if (!door) {
    res.sendStatus(404);
    return;
  }

  fetch(`${floors[door.floor].address}/api/update?door=${door.id}&status=${req.query.status}`)
    .then((res) => res.text())
    .then((text) => res.send(text))
    .catch((err) => res.send(err.message));
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
