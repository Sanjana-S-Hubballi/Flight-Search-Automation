import pytest
import json
import os

@pytest.fixture(scope="session")
def load_test_data():
    with open(os.path.join(os.path.dirname(__file__), "test_data.json")) as f:
        return json.load(f)