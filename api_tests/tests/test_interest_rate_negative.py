import allure
import pytest

import utils
from base_script import ConfigLoader

STEP_1 = "Send an API request to the endpoint: {} with 'interestRate' having a value of '-10' and no additional fees"
STEP_2 = "Verify that the response has the status code of 400"

cl = ConfigLoader()


@allure.title("Calculate Loan - Negative interest rate")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.xfail(reason="The response should be 400 however, it is 200")
def test_valid_interest_rate_zero_no_fees():
    """
    The test case verifies that if the API endpoint: /loan/calculate receives a req with interest set as -10 and no fees,
    then the server should send handle the Invalid request gracefully
    Returns: None
    """
    # Step - 1
    with allure.step(STEP_1.format(cl.calc_uri)):
        loan_repay = utils.calculate_loan(interest=-10)

    # Step - 2
    with allure.step(STEP_2):
        assert loan_repay.status_code == 400
