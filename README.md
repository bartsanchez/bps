# BPS project (Bulk payment system)


## Requirements

[docker](https://www.docker.com/)
[docker-compose](https://docs.docker.com/compose/)

## Notes about the project

- The total time spent was around 9 hours.
- I am fairly proud about this project.
- The main reason for spending so much time was to fullfil my curiosity using async with Django.
- The app should be configured after a LoadBalancer (normally NGINX) for better scalability.
- The app is running 3 Gunicorn sync workers. Could be worth to investigate the usage of asyncs workers.
- Everything is prepared to use a shared Redis instance for locking (semaphore) and avoiding race conditions so scaling
  horizontally should be safe with the current implementation.
- It is assumed that once created the Transfer instance, some asynchrounous task (Celery?) should perform the real
  bank transfer, and ensure it was successfully performed. Skipped here in purpose.
- This is a git repository, so it could be worth it to review the commit history.

## Usage

Ensure the app is not running:

```sh
make stop
```

Start the application:

```sh
make build
make start
```

## Run tests

Unit tests:

```sh
make tests
```

Integration tests:

```sh
make integration_tests
```
