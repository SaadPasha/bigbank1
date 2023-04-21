import allure
import pytest

import utils
from base_script import ConfigLoader

STEP_1 = "Send an API request to the endpoint: {} with value for the key, 'conclusion' as: {}"
STEP_2 = "Verify that the response has a status code of {} and the JSON schema is as expected"

cl = ConfigLoader()


@allure.title("Calculate Loan - Validation checks for the key 'conclusionFee'")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("conclusion_fee, expected", [(695.80, 200),
                                                      ([12], 400),
                                                      ({"12": 12}, 400),
                                                      ("LOAN2", 400)])
def test_valid_checks_key_admin_fee(conclusion_fee, expected):
    """
    The test case verifies that if the API endpoint: /loan/calculate receives a req with invalid value for conclusionFee key,
    then the server should send handle the Invalid request gracefully
    Returns: None
    """
    # Step - 1
    with allure.step(STEP_1.format(cl.calc_uri, conclusion_fee)):
        loan_repay_invalid_concl_fee_key_resp = utils.calculate_loan(concl_fee=conclusion_fee)

    # Step - 2
    with allure.step(STEP_2.format(expected)):
        assert loan_repay_invalid_concl_fee_key_resp.status_code == expected
        if loan_repay_invalid_concl_fee_key_resp.status_code == 400:
            utils.assert_schema(resp_data=loan_repay_invalid_concl_fee_key_resp.json(), schema_file_name='calculate_resp_invalid.json')
