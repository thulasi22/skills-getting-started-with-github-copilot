import copy
import pytest

from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    # Use TestClient for the FastAPI app
    client = TestClient(app_module.app)
    yield client


@pytest.fixture(autouse=True)
def reset_activities():
    # Make a deep copy of the original activities and restore after test
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
