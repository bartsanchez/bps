# BPS project (Bulk payment system)


## Requirements

[docker](https://www.docker.com/)
[docker-compose](https://docs.docker.com/compose/)

## Notes about the project

- This is an exploratory project and should not be used in production.
- The total time spent was around 9 hours.
- I am fairly proud about this project.
- The main reason for spending so much time was to fullfil my curiosity using async with Django.
- The app should be configured after a LoadBalancer (normally NGINX) for better scalability.
- The app is running 3 Gunicorn sync workers. Could be worth to investigate the usage of asyncs workers.
- Everything is prepared to use a shared Redis instance for locking (semaphore) and avoiding race conditions so scaling
  horizontally should be safe with the current implementation.
- It is assumed that once created the Transfer instance, some asynchrounous task (Celery?) should perform the real
  bank transfer, and ensure it was successfully performed. Skipped here in purpose.
- It is highly recommended to use a better way of handling secrets.
- There is no mention about currency. I am assuming EUR since it's my normal currency but this project is
  currency-agnostic. Note there are no support for multiple currencies.
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

## Manual tests

Wait for the app the be ready, you can see progress with:

```sh
make ps
make logs
```

Then you could test the API in port 8000 of your machine.
There is an already created account. Its balance is: 7777777 cents.

* Note that the API expected an string for the amount, being the value the full amount (not cents).
* Note(2) that if you try to run the exact same payload the API will return error. This is so for avoiding processing
  duplicated requests more than once.

```sh
curl -w "%{http_code}" -X POST -d '{"organization_name": "ACME Corp", "organization_iban": "FR10474608000002006107XXXXX", "organization_bic": "OIVUSCLQXXX", "credit_transfers": [{"amount": "700", "counterparty_name": "d", "counterparty_bic": "e", "counterparty_iban": "f", "description": "g"}]}' -H "Content-Type: application/json" http://localhost:8000/bulk_transfer
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
