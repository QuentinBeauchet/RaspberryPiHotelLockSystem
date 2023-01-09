const express = require("express");
var cors = require("cors");
const fetch = require("node-fetch");
const fs = require("fs");
var app = express();

const port = 3000;

app.use(cors());

const floors = JSON.parse(fs.readFileSync(`../floors.json`));
const doors = JSON.parse(fs.readFileSync(`../doors.json`));

app.get("/api/:door/:status", (req, res) => {
  const door = doors[req.params.door];
  if (!door) {
    res.sendStatus(404);
    return;
  }

  const { address, port } = floors[door.floor];
  fetch(`${address}:${port}/api/${door.id}/${req.params.status}`)
    .then((res) => res.text())
    .then((text) => res.send(text))
    .catch((err) => res.send(err.message));
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
