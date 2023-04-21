import allure
import pytest

import utils
from ui_tests.pom import locators

STEP_1 = "Add alphabetic characters in the input box."
STEP_2 = "Add special characters in the input box"
STEP_3 = "Add more than 14 integers in the input box."
STEP_4 = "Add 14 integers precisely and click outside the input box."
STEP_5 = "Add more than 2 numbers after a decimal place."
STEP_6_a = "Add less than 5 integers and click outside the input box."
STEP_6_b = "Add zero '0' and click outside the input box."


@pytest.mark.parametrize('input_box', [locators.LOAN_AMOUNT_BOX, locators.LOAN_PERIOD_BOX])
@allure.title("Calculate Loan - UI Validations - Loan amount and Loan Period text boxes")
@allure.severity(allure.severity_level.CRITICAL)
def test_loan_and_mon_period_input_validations(open_calc_page_and_modal, calc_page_functions, logger, input_box):
    """
    The test case verifies the UI validations for the "loan amount" and "monthly period" input boxes.
    Args:
        calc_page_functions: Object of calc_page class loaded as fixture
        logger: Logger object loaded as fixture
        input_box: Locator to identify the input box, loaded as fixture due to the
                    parametrization so both boxes can be tested

    Returns: None
    """

    with allure.step(STEP_1):
        rand_str = utils.gen_rand_str(5)
        logger.info("Adding the random string {rand_str} to the loan amount input box...")
        input_data = calc_page_functions.add_data_input_box(input_locator=input_box, data=rand_str)
        assert input_data.input_value() == ""
        logger.info("Verified that the input is blocked...")

    with allure.step(STEP_2):
        special_chars = ['@', '#', '$', '%', '&', '*', '-', '+', '=', '!', '?', ':', ';', '/', '|', '{', '}', '[', ']', '(', ')', '.', ',', '<', '>', '^', '~']
        for s_char in special_chars:
            logger.info("Adding the special character {s_char} to the loan amount input box...")
            input_data = calc_page_functions.add_data_input_box(input_locator=input_box, data=s_char)
            if s_char != ',' and s_char != '.':
                assert input_data.input_value() == ''
                logger.info("Verified that the input is blocked...")
            else:
                assert input_data.input_value() == '0,'
                logger.info("Verified that the input is allowed for the ',' character")

    with allure.step(STEP_3):
        more_than_14_chars = str(utils.gen_rand_int(100000000000000, 999999999999999))
        logger.debug(f"Adding a string of more than 14 numbers, {more_than_14_chars} to the input box...")
        input_data = calc_page_functions.add_data_input_box(input_box, data=more_than_14_chars)
        assert input_data.input_value() == more_than_14_chars[:-1]
        logger.info("Verified that the input is blocked...")

    with allure.step(STEP_4):
        _14_chars = str(utils.gen_rand_int(10000000000000, 99999999999999))
        logger.debug("Adding a string of exactly 14 numbers, {_14_chars} to the input box...")
        input_data = calc_page_functions.add_data_input_box(input_box, data=_14_chars)
        calc_page_functions.page.click(locators.LOAN_MODAL_BODY)
        if input_box == locators.LOAN_AMOUNT_BOX:
            calc_page_functions.page.click(locators.LOAN_MODAL_BODY)
            assert input_data.input_value().replace('\xa0', ' ') == '250 000'
            logger.info("Verified that input box is updated to the max amount i.e. 250 000.")
        else:
            calc_page_functions.page.click(locators.LOAN_MODAL_BODY)
            assert input_data.input_value() == '144'

    with allure.step(STEP_5):
        num_more_than_2_dec_places = "140200,923"
        logger.info("Adding a string with a number having more than 3 decimal places")
        input_data = calc_page_functions.add_data_input_box(input_box, data=num_more_than_2_dec_places)
        assert input_data.input_value() == num_more_than_2_dec_places[:-1]
        logger.info("Verified that the input is blocked...")

    if input_box == locators.LOAN_AMOUNT_BOX:
        with allure.step(STEP_6_a):
            less_than_5_chars = str(utils.gen_rand_int(1000, 9999))
            logger.info("Adding a string with a number less than 5 integers: {less_than_5_chars}")
            input_data = calc_page_functions.add_data_input_box(input_box, data=less_than_5_chars)
            calc_page_functions.page.click(locators.LOAN_MODAL_BODY)
            assert input_data.input_value().replace('\xa0', ' ') == "10 000"
            logger.info("Verified that input box is updated to the min amount i.e. 10 000.")

    else:
        with allure.step(STEP_6_b):
            logger.info("Adding the zero character as a value '0'")
            input_data = calc_page_functions.add_data_input_box(input_box, data='0')
            calc_page_functions.page.click(locators.LOAN_MODAL_BODY)
            assert input_data.input_value() == '12'
            logger.info("Verified that input box is updated to the min monthly period i.e. 12.")
