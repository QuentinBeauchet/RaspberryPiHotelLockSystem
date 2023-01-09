const express = require("express");
var cors = require("cors");
const fs = require("fs");
var app = express();

const floors = JSON.parse(fs.readFileSync(`../floors.json`));

const floor = floors[process.env.floor];

if (!floor) {
  console.log("Floor invalid");
  return;
}

app.use(cors());

app.get("/api/:door/:status", (req, res) => {
  const door = floor.doors[req.params.door];
  if (!door || !["open", "close"].includes(req.params.status)) {
    res.sendStatus(404);
    return;
  }
  res.send(
    `<h1>Floor: n°${process.env.floor}<h1><h2>Door: n°${req.params.door}</h2><h3>Status: ${req.params.status}</h3>`
  );
});

app.listen(floor.port, () => {
  console.log(`Example app listening on port ${floor.port}`);
});
