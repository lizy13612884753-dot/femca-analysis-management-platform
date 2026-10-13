import pytest
import requests
from unittest.mock import patch

from api_client import get_equipment

pytestmark = pytest.mark.regression


def test_get_equipment_timeout(caplog):

    with patch(
        "api_client.requests.get",
        side_effect=requests.exceptions.Timeout
    ):

        with pytest.raises(requests.exceptions.Timeout):
            get_equipment()

    assert "Equipment API request timed out" in caplog.text

def test_get_equipment_connection_error(caplog):

    with patch(
        "api_client.requests.get",
        side_effect=requests.exceptions.ConnectionError
    ):

        with pytest.raises(requests.exceptions.ConnectionError):
            get_equipment()

    assert "Equipment API connection failed" in caplog.text