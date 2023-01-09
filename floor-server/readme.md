# Build with

```zsh
docker-compose build
```

# Start with

```zsh
docker-compose up -d
```

or

```zsh
PORT=3002 FLOOR="1er etage" npm start
```

# Routes

> /api/update?door=`...`&status=`...`

Change the status of a lock to `open` or `close` using the door `id`

> /api/picture?rfid=...

Get the `picture` from an user using his rfid `id`
