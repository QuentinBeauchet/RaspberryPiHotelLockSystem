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
PORT=3000 FLOOR="1er etage" npm start
```

# Routes

> `GET`/api/open?door_id=`...`

Open the door with the id `door_id`.

> `GET` /api/status?door_id=`...`

Get the requested status of the door with the id `door_id` it will be either `true` or `false`, if `true` it will be set to `false` after the request.

> `GET` /api/user?door_id=`...`&rfid=`...`

Will fetch the `user` of the `rfid` if he has the `permissions` to open the door with this `door_id`.

> `POST` /api/user/add?rfid=`...`&first%20name=`...`&last%20name=`...`&picture=`...`

Add the `user` with his informations to the DB.

> `GET` /api/admins

Get the `admins` in the DB.

# Test with

> http://localhost:3000/api/open?door_id=1

Open the door using the API.

> http://localhost:3000/api/status?door_id=1

Get the door status.
