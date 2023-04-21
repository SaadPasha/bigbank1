import pytest

from ui_tests.pom.calc_page import CalcPage
from ui_tests.pom import locators
from playwright.sync_api import Page
from logger import logging_setup


@pytest.fixture(scope="function")
def calc_page_functions(page: Page):
    return CalcPage(page)


@pytest.fixture(scope="function")
def open_calc_page_and_modal(calc_page_functions):
    calc_page_functions.load_calc_page()
    calc_page_functions.open_calc_modal(locators.CALC_BUTTON)
    return True


@pytest.fixture(scope="session")
def logger():
    logger = logging_setup()
    return logger
