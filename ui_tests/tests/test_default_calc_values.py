import allure
import pytest

from ui_tests.pom import locators

STEP_1 = '"With the modal view opened the first time, verify the following:\nLoan amount set to 85000 KR." \
         "\nLoan period set to 120 months\nMonthly Repayable amount set to 1168,47 SEK.\nInterest rate set as 10.95%"'
STEP_2 = "Now Update the loan amount to 95000, and note the Loan repayment changed."
STEP_3 = "Then set back to default i.e. 85000 and match that Loan repayment is same with the one in step 1."


@pytest.mark.xfail(strict=False, reason="The repay amount is different in the third step even though loan amount is same as first step")
@allure.title("Calculate Loan - Default view of the modal and calculations")
@allure.severity(allure.severity_level.BLOCKER)
def test_default_vals(open_calc_page_and_modal, calc_page_functions, logger):
    """
    The test case verifies that the default view of the modal has some predefined values in the input boxes and labels.
    Also, that the default values of the modal will be
    Returns: None
    """
    with allure.step(STEP_1):
        default_loan_amount = calc_page_functions.page.locator(locators.LOAN_AMOUNT_BOX).input_value()
        default_loan_period = calc_page_functions.page.locator(locators.LOAN_PERIOD_BOX).input_value()
        default_monthly_repay = calc_page_functions.page.locator(locators.REPAY_AMOUNT).inner_text()
        default_monthly_repay = default_monthly_repay.replace(' ', '').replace('SEK', '').replace('\n', '').replace('\xa0', ' ').replace('\xa0', ' ').replace(' ', '')
        default_interest_rate = calc_page_functions.page.wait_for_selector(locators.INTEREST_RATE).inner_text()

        assert default_loan_amount.replace('\xa0', ' ') == '85 000'
        assert default_loan_period == '120'
        assert default_monthly_repay == '1168,47'
        assert default_interest_rate[:-1] == '10.95'
        logger.info("Verified that hte default values are as expected on opening the modal.")

    with allure.step(STEP_2):
        new_amount = calc_page_functions.add_data_input_box(input_locator=locators.LOAN_AMOUNT_BOX, data="95000")
        calc_page_functions.page.click(locators.LOAN_MODAL_BODY)
        assert new_amount.input_value().replace("\xa0", " ") == "95 000"

        calc_page_functions.page.is_visible(locators.REPAY_AMOUNT, timeout=10000)
        new_monthly_repay = calc_page_functions.page.wait_for_selector(locators.REPAY_AMOUNT).inner_text()
        new_monthly_repay = new_monthly_repay.replace(' ', '').replace('SEK', '').replace('\n', '').replace('\xa0', ' ').replace('\xa0', ' ').replace(' ', '')
        assert new_monthly_repay != default_monthly_repay
        logger.info("Verified that by adding new loan amount, the monthly repay amount is also changed.")

    with allure.step(STEP_3):
        back_to_default_amount = calc_page_functions.add_data_input_box(input_locator=locators.LOAN_AMOUNT_BOX, data="85000")
        calc_page_functions.page.click(locators.LOAN_MODAL_BODY)
        assert back_to_default_amount.input_value().replace('\xa0', ' ') == "85 000"

        calc_page_functions.page.is_visible(locators.REPAY_AMOUNT, timeout=10000)
        back_to_default_repay_amount = calc_page_functions.page.wait_for_selector(locators.REPAY_AMOUNT).inner_text()
        back_to_default_repay_amount = back_to_default_repay_amount.replace(' ', '').replace('SEK', '').replace('\n', '').replace('\xa0', ' ').replace('\xa0', ' ').replace(' ', '')
        print("DEFAULT UPDATED: " + back_to_default_repay_amount)
        assert back_to_default_repay_amount == default_monthly_repay
        logger.info("Verified that the setting the loan amount back to the default one generates the repay amount similar to default as well.")
