import pytest
import time


@pytest.fixture(scope="function", autouse=True)
def sleeper():
    """
    Fixture to add some wait time between each test execution
    Returns: None
    """
    time.sleep(5)
