import allure

import utils
from base_script import ConfigLoader

STEP_1 = "Send an API request to the endpoint: {} with default values"
STEP_2 = "Verify that the response has a status code of 200 and the JSON schema is valid"

cl = ConfigLoader()


@allure.title("Calculate Loan - Valid request parameters and JSON schema validation")
@allure.severity(allure.severity_level.BLOCKER)
def test_valid_req_and_json_validation():
    """
    The test case verifies that if the API endpoint: /loan/calculate receives a req with valid params,
    then the server should send a valid JSON response
    Returns: None
    """
    # Step - 1
    with allure.step(STEP_1.format(cl.calc_uri)):
        loan_repay = utils.calculate_loan()

    # Step - 2
    with allure.step(STEP_2):
        assert loan_repay.status_code == 200
        utils.assert_schema(resp_data=loan_repay.json())
