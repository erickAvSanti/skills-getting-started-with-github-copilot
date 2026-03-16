from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


BASE_ACTIVITIES = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities_state(monkeypatch):
    monkeypatch.setattr(app_module, "activities", deepcopy(BASE_ACTIVITIES))


@pytest.fixture
def client():
    return TestClient(app_module.app)
