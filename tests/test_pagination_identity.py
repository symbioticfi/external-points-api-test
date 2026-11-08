import json

import pytest
import requests

import test_all_points
from config_data import TestConfig


class OfflineClient:
    def __init__(self, rows, ignore_offset=False):
        self.rows = rows
        self.ignore_offset = ignore_offset

    def get_all_points(self, block_number, offset, limit):
        assert block_number == TestConfig.BLOCK_NUMBER
        if self.ignore_offset:
            offset = 0
        response = requests.Response()
        response.status_code = 200
        response._content = json.dumps(self.rows[offset:offset + limit]).encode()
        return response


@pytest.fixture(autouse=True)
def forbid_live_requests(monkeypatch):
    def fail_request(*args, **kwargs):
        pytest.fail("Offline regression must not make live API requests")

    monkeypatch.setattr(requests, "request", fail_request)


@pytest.mark.parametrize(
    "points_type, dimension",
    [("network", "network_address"), ("network", "receiver_type"),
     ("vault", "receiver_type")],
)
def test_pagination_preserves_record_identity(monkeypatch, points_type, dimension):
    monkeypatch.setattr(TestConfig, "POINTS_TYPE", points_type)
    monkeypatch.setattr(TestConfig, "SUPPORTED_RECEIVER_TYPES", ["staker", "operator"])
    rows = []
    for index in range(8):
        row = {
            "receiver_type": "staker",
            "receiver_address": "0x" + "1" * 40,
            "vault_address": "0x" + "2" * 40,
            "points": 100,
            "block_number": TestConfig.BLOCK_NUMBER,
        }
        if points_type == "network":
            row["network_address"] = "0x" + "3" * 40
        if dimension == "network_address":
            row[dimension] = f"0x{index + 1:040x}"
        else:
            row[dimension] = ["staker", "operator"][index % 2]
            row["vault_address"] = f"0x{index // 2 + 1:040x}"
        rows.append(row)

    client = OfflineClient(rows)
    suite = test_all_points.TestAllPoints()
    suite.test_get_all_points_success(client)
    suite.test_get_all_points_pagination(client)

    # Retaining every identity field must not let a broken offset pass.
    with pytest.raises(AssertionError, match="Offset or limit"):
        suite.test_get_all_points_pagination(OfflineClient(rows, ignore_offset=True))
