import allure

import utils
from base_script import ConfigLoader

STEP_1 = "Send an API request to the endpoint: {} with 'interestRate' having a value of '0' and no additional fees"
STEP_2 = "Verify that the response has the total repayment amount is equal to the one that is borrowed and APR is 0"

cl = ConfigLoader()


@allure.title("Calculate Loan - API response for the interest rate of 0 and no additional fees")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_interest_rate_zero_no_fees():
    """
    The test case verifies that if the API endpoint: /loan/calculate receives a req with interest set as 0 and no fees,
    then the server should send a valid JSON response where the return amount is same as borrowed amount
    Returns: None
    """
    # Step - 1
    with allure.step(STEP_1.format(cl.calc_uri)):
        amount = 120000
        loan_repay = utils.calculate_loan(period=1, amount=amount, admin_fee=0, concl_fee=0, interest=0)

    # Step - 2
    with allure.step(STEP_2):
        assert loan_repay.status_code == 200
        assert loan_repay.json()['totalRepayableAmount'] == amount
        assert loan_repay.json()['apr'] == 0
