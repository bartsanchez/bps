from pathlib import Path

import requests

BASE_URL = "http://bps:8000"
ADMIN_URL = f"{BASE_URL}/admin"
BULK_TRANSFER_URL = f"{BASE_URL}/bulk_transfer"

CREATED_STATUS_CODE = 201
UNPROCESSABLE_CONTENT_STATUS_CODE = 422


def test_sample1():
    with Path("./sample1.json").open() as f:
        data = f.read()

    r = requests.post(BULK_TRANSFER_URL, data=data, timeout=5)
    assert r.status_code == CREATED_STATUS_CODE


def test_sample1_again_is_returning_422_error():
    with Path("./sample1.json").open() as f:
        data = f.read()

    r = requests.post(BULK_TRANSFER_URL, data=data, timeout=5)
    assert r.status_code == UNPROCESSABLE_CONTENT_STATUS_CODE


def test_sample2__not_enough_funds():
    with Path("./sample2.json").open() as f:
        data = f.read()

    r = requests.post(BULK_TRANSFER_URL, data=data, timeout=5)
    assert r.status_code == UNPROCESSABLE_CONTENT_STATUS_CODE  # not enough funds
