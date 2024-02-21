import json
from pathlib import Path

import requests

BASE_URL = "http://bps:8000"
ADMIN_URL = f"{BASE_URL}/admin"
BULK_TRANSFER_URL = f"{BASE_URL}/transfers/bulk_transfer"

UNPROCESSABLE_CONTENT_STATUS_CODE = 422


def test_samples():
    for sample_name in ("sample1.json", "sample2.json"):
        with Path(f"./{sample_name}").open() as f:
            sample_content = f.read()

        data = json.loads(sample_content)

        r = requests.post(BULK_TRANSFER_URL, data=data, timeout=5)
        assert r.status_code == requests.codes.ok


def test_sample1_again_is_returning_422_error():
    with Path("./sample1.json").open() as f:
        sample_content = f.read()

    data = json.loads(sample_content)

    r = requests.post(BULK_TRANSFER_URL, data=data, timeout=5)
    assert r.status_code == UNPROCESSABLE_CONTENT_STATUS_CODE
