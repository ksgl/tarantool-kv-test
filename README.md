# An HTTP-server to serve a key-value database (Tarantool).

### Build Instructions
Assuming you've cloned this repo:
```
docker build . -t tarantool-api-server
docker run -p 8888:8888 --name tarantool-api-server -t tarantool-api-server
```
Now you have your server available at `http://localhost:8888`

### API
Method   | Path     | Body                                          | Response                               |
-------- | -------- | --------------------------------------------- | -------------------------------------- |
POST     | /kv      | {"key":<string>, "value":<arbitrarty_json>}   | 200 OK, 400 Bad Request, 409 Conflict  |
PUT      | /kv/{id} | {"value":<arbitrarty_json>}                   | 200 OK, 400 Bad Request, 404 Not Found |
GET      | /kv/{id} | none                                          | 200 OK, 404 Not Found | 
DELETE   | /kv/{id} | none                                          | 200 OK, 404 Not Found |
