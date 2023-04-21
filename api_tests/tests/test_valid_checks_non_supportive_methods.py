import allure
import pytest

import utils
from base_script import ConfigLoader

cl = ConfigLoader()

STEP_1 = "Verify that an API request to endpoint: {} with method: {} results in response code of 404"
STEP_2 = "Verify that the resp body has the error in the response"


@allure.title("Calculate Loan - Validation checks for the non-supportive methods")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("req_method, expected", [("GET", 404), ("PUT", 404),
                                                  ("PATCH", 404), ("DELETE", 404)])
def test_incorrect_methods_and_invalid_headers(req_method, expected):
    """
    The testcase verifies that if the API endpoint receives a request with Non-Supported method call,
    then it should respond with a response code of 404.
    Returns: None
    """
    # Step - 1
    with allure.step(STEP_1.format(cl.calc_uri, req_method)):
        assert utils.invalid_req_methods(req_method, cl.calc_uri).status_code == expected
