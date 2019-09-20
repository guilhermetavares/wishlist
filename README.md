
# Wishlist for Magalu

To follow and run this instructions, you need a (https://www.docker.com/get-started)[Docker] installed.
You can run using some virtualenv.

The api is protected by basic auth, you can validate on this credentials
```
username: user
password: password
```

First, you need build the container, for this use the command
```
make build
```

To run the project, the api is server on http://0.0.0.0:4000/.
After run, you access the docs in http://0.0.0.0:4000/docs

```
make run
```

This project contains units tests, to run it, you need to run
```
make test
```
