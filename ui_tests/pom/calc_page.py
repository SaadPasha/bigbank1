import locators
from playwright.sync_api import Page
from base_script import ConfigLoader
from logger import logging_setup


cl = ConfigLoader()
logger = logging_setup()


class CalcPage:

    def __init__(self, page: Page) -> None:
        self.page = page

    def load_calc_page(self):
        """
        Loads homepage
        Returns: None
        """
        self.page.goto(cl.loan_page_url)
        logger.debug("Opening the homepage with URL: {}".format(cl.loan_page_url))

    def open_calc_modal(self, calc_locator):
        """
        Opens calculator modal using click
        Args:
            calc_locator: button to click
        Returns: True
        """
        self.page.click(calc_locator)
        self.page.wait_for_selector(calc_locator)
        logger.debug("Opening the modal")
        return True

    def close_calc_modal(self, calc_locator=locators.CAL_OVERLAY, close_button_locator=locators.CLOSE_BUTTON):
        """
        Closes the calculator modal button
        Args:
            calc_locator:
            close_button_locator: Button locator to be use for closing the modal
        Returns: None
        """
        self.page.click(close_button_locator)
        logger.debug("Closing the modal")
        self.page.wait_for_selector(calc_locator, state='hidden')
        return True

    def add_data_input_box(self, input_locator, data):
        """
        Adds the input data to the input box
        Args:
            input_locator: Input box to add input-data
            data: Input data to add
        Returns: None
        """
        input_box = self.page.locator(input_locator)
        input_box.click()
        input_box.clear()
        input_box.type(data)
        return input_box
