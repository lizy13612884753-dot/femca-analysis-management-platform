import os
import pytest
from api_client import login, get_equipment_types
import requests
import logging



logger = logging.getLogger(__name__)


login_data = {
    "username": os.getenv("FEMCA_USERNAME"),
    "password": os.getenv("FEMCA_PASSWORD")
}

@pytest.fixture(scope="session")
def access_token():
    login_response = login(
        login_data["username"],
        login_data["password"]
    )

    assert login_response.status_code == 200

    token = login_response.json()["tokens"]["access"]

    return token

@pytest.fixture
def authenticated_session(access_token):
    with requests.Session() as session:
        session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })

        yield session


@pytest.fixture(scope="session")
def equipment_type_id(access_token):
    response = get_equipment_types(access_token)
    data = response.json()

    assert response.status_code == 200
    assert len(data["results"]) > 0

    equipment_type_id = data["results"][0]["id"]

    return equipment_type_id


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        logger.error(
            "Test FAILED: %s\nReason:\n%s",
            item.nodeid,
            report.longreprtext
        )
