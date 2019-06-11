# Homework

Please create an HTTP client program that can execute requests against the API server in this repo.

To run the API server:

1. Ensure you have a valid version of Python 3.6+ installed
2. Clone this repository: 
```
$ git clone https://github.com/secberus/homework-api
```
3. Run the server
```
$ cd homework-api
$ ./run.py
```

## Requirements:

Please use Python3 (3.6+).

Create an HTTP client application that can execute the following HTTP requests sequentially against the server.

1. `GET http://localhost:5000/api/secret1`
2. `GET http://localhost:5000/api/secret2`
3. `GET http://localhost:5000/api/secret3`

You'll first need to login to the server by executing a `POST` request to the authentication endpoint at `http://localhost:5000/api/login`.

The authentication payload should be exactly this:
```
{
  "username": "guest",
  "password": "guest"
}
```

A successful login request will result in a response from the server with the following format:
```
{
  "access_token": "89a35947-5360-4731-9b69-f8d683c4d778"
}
```

The value of the `access_token` must be included in the standard `Authorization` header in the `GET` requests above.

```
Authorization: Bearer <access_token_value>
```

The `access_token` is only good for a short period, after which time, your client will have to authenticate again to continue querying the `GET` API URIs.  Please ensure your client program will gracefully handle the `401: Unauthorized` response status from the API and re-authenticate.

Your solution is complete when you can issue all three `GET` requests above, and get `200 OK` responses from the server without any manual intervention.

## Hints:

* Secberus uses the “aiohttp" library internally for creating HTTP clients and servers.
* Extra credit for making unit tests for your application (we use pytest).  Look up “Test Driven Development" (TDD).
* We run "pylint" and "mypy" internally to check code quality.

## Solution:

Please commit your solution to an empty repository in your github account and send an email to 'jason@secberus.com' with a link to the repository.  If this is a private repostitory, make sure 'subfxnet' (jason@secberus.com's Github username) is added as a contributor to the repository.

