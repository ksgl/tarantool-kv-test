# An HTTP-server to serve a key-value database (Tarantool)

### Deployment
API lives [here](http://134.209.200.24:8888/kv).

### Build Instructions
Assuming you've cloned this repo:
```
docker build . -t tarantool-api-server
docker run -p 8888:8888 --name tarantool-api-server -t tarantool-api-server
```
Now you have your server available at `http://localhost:8888`

### Testing - Python Unit Tests
To run tests simply do
```
./tests.py
```

### API
Method   | Path     | Body                                          | Response                               |
-------- | -------- | --------------------------------------------- | -------------------------------------- |
POST     | /kv      | {"key":<string>, "value":<arbitrary_json>}   | 200 OK, 400 Bad Request, 409 Conflict  |
PUT      | /kv/{id} | {"value":<arbitrary_json>}                   | 200 OK, 400 Bad Request, 404 Not Found |
GET      | /kv/{id} | none                                          | 200 OK, 404 Not Found |
DELETE   | /kv/{id} | none                                          | 200 OK, 404 Not Found |
