from fastapi.testclient import TestClient

from server import app


HCP_API = "api/hcps"

# TODO tests currently test against prod db - need to setup testing db
# TODO abstract test response data for cleanliness


# HCP list API test cases
def test_list_hcps_returns_list_correctly():
    """test list api returns list correctly"""
    with TestClient(app) as client:
        response = client.get(HCP_API)
        assert response.status_code == 200
        assert response.json() == {
            "hcps": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "address_link": {
                        "addr1": "123 Main Street",
                        "addr2": "Suite 101",
                        "city": "New York City",
                        "state": "NY",
                        "zip": "10001",
                        "status": "A",
                    },
                    "status": "A",
                    "countryIsoCode": "US",
                },
                {
                    "id": 2,
                    "name": "Jane Smith",
                    "address_link": {
                        "addr1": "456 Park Avenue",
                        "addr2": None,
                        "city": "Los Angeles",
                        "state": "CA",
                        "zip": "90001",
                        "status": "A",
                    },
                    "status": "A",
                    "countryIsoCode": "US",
                },
                {
                    "id": 3,
                    "name": "Emily Adams",
                    "address_link": {
                        "addr1": "101 Second Avenue",
                        "addr2": None,
                        "city": "Houston",
                        "state": "TX",
                        "zip": "77001",
                        "status": "A",
                    },
                    "status": "I",
                    "countryIsoCode": "US",
                },
            ]
        }


# TODO this test would be expanded in line with fuzzysearch functionality
def test_list_hcps_returns_filtered_list_correctly():
    """test list api returns filtered list correctly"""
    with TestClient(app) as client:
        response = client.get(f"{HCP_API}?search=John+Doe")
        assert response.status_code == 200
        assert response.json() == {
            "hcps": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "address_link": {
                        "addr1": "123 Main Street",
                        "addr2": "Suite 101",
                        "city": "New York City",
                        "state": "NY",
                        "zip": "10001",
                        "status": "A",
                    },
                    "status": "A",
                    "countryIsoCode": "US",
                }
            ]
        }


def test_list_hcps_returns_filtered_empty_list_correctly():
    """test list api returns empty filtered list correctly"""
    # Note: endpoint should not throw error -
    # returning an empty list if no search results is a valid response.
    with TestClient(app) as client:
        response = client.get(f"{HCP_API}?search=George")
        assert response.status_code == 200
        assert response.json() == {"hcps": []}


# HCP detail API test cases
def test_detail_hcps_returns_item_correctly():
    """test detail api returns item correctly"""
    test_id = 1
    with TestClient(app) as client:
        response = client.get(f"{HCP_API}/{test_id}")
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "John Doe",
            "address_link": {
                "addr1": "123 Main Street",
                "addr2": "Suite 101",
                "city": "New York City",
                "state": "NY",
                "zip": "10001",
                "status": "A",
            },
            "status": "A",
            "countryIsoCode": "US",
            "affiliations": [
                {
                    "child_link": {
                        "id": 2,
                        "name": "Jane Smith",
                        "address_link": {
                            "id": 2,
                            "parent_link": 2,
                            "parent_type": "HCP",
                            "addr1": "456 Park Avenue",
                            "addr2": None,
                            "city": "Los Angeles",
                            "state": "CA",
                            "zip": "90001",
                            "status": "A",
                        },
                        "status": "A",
                        "countryIsoCode": "US",
                    },
                    "status": "A",
                    "type": "HCP_HCP",
                },
                {
                    "child_link": {
                        "id": 3,
                        "name": "Emily Adams",
                        "address_link": {
                            "id": 3,
                            "parent_link": 3,
                            "parent_type": "HCP",
                            "addr1": "789 First Street",
                            "addr2": "Unit B",
                            "city": "Chicago",
                            "state": "IL",
                            "zip": "60601",
                            "status": "I",
                        },
                        "status": "I",
                        "countryIsoCode": "US",
                    },
                    "status": "A",
                    "type": "HCP_HCP",
                },
                {
                    "child_link": {
                        "id": 1,
                        "name": "ABC Hospital",
                        "address_link": {
                            "id": 11,
                            "parent_link": 1,
                            "parent_type": "HCO",
                            "addr1": "100 Hospital Road",
                            "addr2": None,
                            "city": "New York City",
                            "state": "NY",
                            "zip": "10001",
                            "status": "A",
                        },
                        "status": "A",
                    },
                    "status": "A",
                    "type": "HCP_HCO",
                },
            ],
        }


def test_detail_hcps_throws_error_if_item_not_found():
    """test detail api throws error if item not found"""
    test_id = 7
    with TestClient(app) as client:
        response = client.get(f"{HCP_API}/{test_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": f"[get_hcp()] Hcp {test_id} not found"}
