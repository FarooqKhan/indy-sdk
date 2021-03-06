from tests.utils import storage
from indy import ledger
from indy.error import ErrorCode, IndyError

import json
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(autouse=True)
def before_after_each():
    storage.cleanup()
    yield
    storage.cleanup()


@pytest.mark.asyncio
async def test_build_node_request_works_for_missed_field_in_data_json():
    identifier = "identifier"
    destination = "destination"
    data = {
        "node_ip": "ip",
        "node_port": 1,
        "client_ip": "ip",
        "client_port": 1
    }

    with pytest.raises(IndyError) as e:
        await ledger.build_node_request(identifier, destination, json.dumps(data))
    assert ErrorCode.CommonInvalidStructure == e.value.error_code


@pytest.mark.asyncio
async def test_build_node_request_works_for_correct_data_json():
    identifier = "identifier"
    destination = "destination"
    data = {
        "node_ip": "ip",
        "node_port": 1,
        "client_ip": "ip",
        "client_port": 1,
        "alias": "some",
        "services": ["VALIDATOR"]
    }

    expected_response = {
        "identifier": identifier,
        "operation": {
            "type": "0",
            "dest": destination,
            "data": data
        }
    }

    response = json.loads(await ledger.build_node_request(identifier, destination, json.dumps(data)))
    assert expected_response.items() <= response.items()
