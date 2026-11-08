import pytest
from config_data import TestConfig
from utils import is_ethereum_address


class TestAllPoints:
    def test_get_all_points_success(self, api_client):
        """Test successful retrieval of all points"""
        response = api_client.get_all_points(TestConfig.BLOCK_NUMBER, offset=0, limit=2)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Should return a list"
        assert len(data) == 2, "Should return 2 entities"


        assert all("points" in entity for entity in data), "points should be in response"
        assert all(isinstance(entity["points"], int) for entity in data), "points should be a integer"
        assert all(entity["points"] > 0 for entity in data), "points should be greater than 0"

        assert all("block_number" in entity for entity in data), "block_number should be in response"
        assert all(isinstance(entity["block_number"], int) for entity in data), "block_number should be a integer"
        assert all("receiver_type" in entity for entity in data), "receiver_type should be in response"
        assert all(entity["receiver_type"] in TestConfig.SUPPORTED_RECEIVER_TYPES for entity in
                   data), "receiver type should be supported"
        assert all("receiver_address" in entity for entity in data), "receiver_address should be in response"
        assert all(is_ethereum_address(entity["receiver_address"]) for entity in data), "receiver_address should be a valid ethereum address"

        assert all("vault_address" in entity for entity in data), "vault_address should be in response"
        assert all(is_ethereum_address(entity["vault_address"]) for entity in data), "vault_address should be a valid ethereum address"

        if TestConfig.POINTS_TYPE == "network":
            assert all("network_address" in entity for entity in data), "network_address should be in response"
            assert all(is_ethereum_address(entity["network_address"]) for entity in data), "network_address should be a valid ethereum address"

    def test_get_all_points_pagination(self, api_client):
        """Test pagination of all points"""
        first_page = api_client.get_all_points(TestConfig.BLOCK_NUMBER, offset=0, limit=4)
        second_page = api_client.get_all_points(TestConfig.BLOCK_NUMBER, offset=2, limit=4)
        third_page = api_client.get_all_points(TestConfig.BLOCK_NUMBER, offset=4, limit=4)

        first_page_data, second_page_data, third_page_data = first_page.json(), second_page.json(), third_page.json()

        assert first_page.status_code == 200
        assert second_page.status_code == 200
        assert third_page.status_code == 200


        def record_set(page):
            return {
                (
                    item["receiver_type"],
                    item["receiver_address"],
                    item["points"],
                    item["vault_address"],
                    item["network_address"] if TestConfig.POINTS_TYPE == "network" else None,
                )
                for item in page
            }

        first_records = record_set(first_page_data)
        second_records = record_set(second_page_data)
        third_records = record_set(third_page_data)

        assert len(first_records & second_records) == 2, "Offset or limit not working correctly. Should have 2 common records"
        assert len(second_records & third_records) == 2, "Offset or limit not working correctly. should have 2 common records"
        assert len(first_records & third_records) == 0, "Offset or limit not working correctly. should have 0 common records"

    @pytest.mark.parametrize("receiver_type", ["staker", "network", "operator"])
    def test_get_all_points_with_receiver_type(self, api_client, receiver_type):
        """Test all points retrieval with receiver type filter"""
        if receiver_type not in TestConfig.SUPPORTED_RECEIVER_TYPES:
            pytest.skip(f"Points for {receiver_type} are not supported")

        response = api_client.get_all_points(TestConfig.BLOCK_NUMBER, offset=0, limit=10, receiver_type=receiver_type)
        assert response.status_code == 200
        data = response.json()
        assert all(entity["receiver_type"] == receiver_type for entity in data), "receiver_type should match"
