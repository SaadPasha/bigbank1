import allure
import pytest

import utils
from base_script import ConfigLoader

STEP_1 = "Send an API request to the endpoint: {} with value for the key, 'currency' as: {}"
STEP_2 = "Verify that the response has a status code of {} and the JSON schema is as expected"

cl = ConfigLoader()


@allure.title("Calculate Loan - Validation checks for the key 'currency'")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("currency, expected", [(695.80, 400),
                                                ([12], 400),
                                                ({"12": 12}, 400),
                                                ("SEKE", 500)])
def test_valid_checks_key_admin_fee(currency, expected):
    """
    The test case verifies that if the API endpoint: /loan/calculate receives a req with invalid value for currency key,
    then the server should send handle the Invalid request gracefully
    Returns: None
    """
    # Step - 1
    with allure.step(STEP_1.format(cl.calc_uri, currency)):
        loan_repay_invalid_currency_key_resp = utils.calculate_loan(currency=currency)

    # Step - 2
    with allure.step(STEP_2.format(expected)):
        assert loan_repay_invalid_currency_key_resp.status_code == expected
        if loan_repay_invalid_currency_key_resp.status_code == 400:
            utils.assert_schema(resp_data=loan_repay_invalid_currency_key_resp.json(), schema_file_name='calculate_resp_invalid.json')
