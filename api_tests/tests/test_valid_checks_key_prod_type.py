import allure
import pytest

import utils
from base_script import ConfigLoader

STEP_1 = "Send an API request to the endpoint: {} with value for the key, 'productType' as: {}"
STEP_2 = "Verify that the response has a status code of {} and the JSON schema is as expected"

cl = ConfigLoader()


@allure.title("Calculate Loan - Validation checks for the key 'productType'")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("prod_type, expected", [(1000, 400),
                                                 ([1000], 400),
                                                 ({"1000": 1000}, 400),
                                                 (1000.60, 400)])
def test_valid_checks_key_prod_type(prod_type, expected):
    """
    The test case verifies that if the API endpoint: /loan/calculate receives a req with invalid value for productType key,
    then the server should send handle the Invalid request gracefully.
    Returns: None
    """
    # Step - 1
    with allure.step(STEP_1.format(cl.calc_uri, prod_type)):
        loan_repay_invalid_prod_type_key_resp = utils.calculate_loan(prod=prod_type)

    # Step - 2
    with allure.step(STEP_2.format(expected)):
        assert loan_repay_invalid_prod_type_key_resp.status_code == expected
        if loan_repay_invalid_prod_type_key_resp.status_code == 400:
            utils.assert_schema(resp_data=loan_repay_invalid_prod_type_key_resp.json(), schema_file_name='calculate_resp_invalid.json')
