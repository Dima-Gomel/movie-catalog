from collections.abc import Generator

import pytest
from main import app
from starlette.testclient import TestClient


@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client
