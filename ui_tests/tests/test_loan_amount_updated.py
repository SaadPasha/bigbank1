import allure
import pytest

from ui_tests.pom import locators

STEP_1 = "Enter the new amount in the 'Loan amount' input box."
STEP_2 = "Enter the number of months in the 'Loan period' input box."
STEP_3 = "Click on the 'Apply Now' button."
STEP_3_a = "Click on the 'X (Cross)' button."
STEP_4 = "Verify the amount in the top right count with the label 'Loan amount'."


@pytest.mark.parametrize("button", [locators.SAVE_BUTTON,
                                    locators.CLOSE_BUTTON])
@allure.title("Calculate Loan - Amount saved and Not Saved")
@allure.severity(allure.severity_level.BLOCKER)
def test_loan_amount_updated(open_calc_page_and_modal, calc_page_functions, logger, button):
    """
    The test case verifies that the input amount is saved when the "Apply Now"
    button is clicked and the previously applied amount is added as well as that
    its not saved when the cross button or out of greyed out area is clicked.
    Args:
        calc_page_functions:
        logger:

    Returns: None
    """
    with allure.step(STEP_1):
        loan_amount = "120000"
        add_loan_amount = calc_page_functions.add_data_input_box(input_locator=locators.LOAN_AMOUNT_BOX, data=loan_amount)
        assert add_loan_amount.input_value() == "120000"
        logger.info(f"Successfully added loan amount of {loan_amount}")

    with allure.step(STEP_2):
        loan_period = "24"
        add_loan_period = calc_page_functions.add_data_input_box(input_locator=locators.LOAN_PERIOD_BOX, data=loan_period)
        assert add_loan_period.input_value() == "24"
        logger.info(f"Successfully added loan period of {loan_period}")

    if button == locators.SAVE_BUTTON:
        with allure.step(STEP_3):
            calc_page_functions.close_calc_modal(close_button_locator=locators.SAVE_BUTTON)
            logger.info("Calculator Modal closed with 'Apply Now' button")
    else:
        with allure.step(STEP_3_a):
            calc_page_functions.close_calc_modal()

    with allure.step(STEP_4):
        updated_amount = calc_page_functions.page.locator(locators.LOAN_AMOUNT_LABEL).inner_text()
        print(updated_amount)

        if button == locators.SAVE_BUTTON:
            assert updated_amount == loan_amount
        else:
            assert updated_amount == "85000"
