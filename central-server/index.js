const express = require("express");
var cors = require("cors");
const fetch = require("node-fetch");
var app = express();

const port = 5000;

app.use(cors());

const floors = {
  1: "http://localhost:3000",
  2: "http:localhost:3001",
};
const doors = {
  "Conference room": {
    floor: 1,
    id: 1,
  },
  Toilets: {
    floor: 1,
    id: 2,
  },
  "Learning center": {
    floor: 2,
    id: 1,
  },
};

app.get("/api/open", (req, res) => {
  const door = doors[req.query.door];
  if (!door) {
    res.sendStatus(404);
    return;
  }

  fetch(`${floors[door.floor]}/api/open?door_id=${door.id}`)
    .then((res) => res.text())
    .then((text) => res.send(text))
    .catch(() => res.send("<h1>Floor server unavalaible</h1>"));
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
