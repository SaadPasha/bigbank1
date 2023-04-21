import allure
import pytest

import utils
from base_script import ConfigLoader

STEP_1 = "Send an API request to the endpoint: {} with 'monthlyPaymentDay' having a value of '0' and '32'"
STEP_2 = "Verify that the response has the status code of 400"

cl = ConfigLoader()


@allure.title("Calculate Loan - Monthly payment day is more than 31 and less than 1")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("repay_day, expected", [(0, 400),
                                                 (32, 500)])
@pytest.mark.xfail(strict=False, reason="400 is expected, however 500 and 200 is returned for both tests respectively")
def test_valid_interest_rate_zero_no_fees(repay_day, expected):
    """
    The test case verifies that if the API endpoint: /loan/calculate receives a req with date set as 0 and 32 ,
    then the server should send handle the Invalid request gracefully
    Returns: None
    """
    # Step - 1
    with allure.step(STEP_1.format(cl.calc_uri)):
        loan_repay = utils.calculate_loan(repay_day=repay_day)

    # Step - 2
    with allure.step(STEP_2):
        assert loan_repay.status_code == 400
