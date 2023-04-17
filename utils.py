#!/usr/bin/env python3
"""
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
__author__: "Saad Tahir"
__date__: "22/3/2023"
__updated__: ""
__version__ = "1.0"
__maintainer__ = "Saad Tahir"
__email__ = "saad.tahir@ut.ee"
__status__ = "Developed"
# ----------------------------------------------------------------------------
# The script adds the following util methods to be used for the tests:
- Request Method(s)
- Helpers (to load files etc.)
- Calculate endpoint specific
# ----------------------------------------------------------------------------
"""
import json
import os
import random
import string

import requests as re
from jsonschema import validate

from base_script import ConfigLoader
from logger import logging_setup

logger = logging_setup()
cl = ConfigLoader()


# ----------------------------------------------- REQUEST Operations ---------------------------------------------#
#                                                                                                                 #
# ----------------------------------------------------------------------------------------------------------------#
def post_req(uri, protocol, host, headers, data, api_ver):
    """
    Sends a POST request with the specified parameters
    Args:
        uri: the specific URI of the request
        protocol: HTTP/HTTPS protocol to be used (based on config)
        host: host address
        api_ver: the current api ver
        headers: X-road headers
        data: The request body to be sent

    Returns: a Rest object with all the properties to proceed for tests
    """
    resp_post = request_operation(req_method='POST', uri=uri, protocol=protocol, host=host,
                                  api_ver=api_ver, data=data, headers=headers)
    return resp_post


def request_operation(req_method, uri, protocol, host, headers, data=None, api_ver=None):
    """
    Method to send the api_tests request using the 'requests' library object.
    Args:
        req_method: specifies the method for the api_tests request to be sent i.e. GET or POST etc.
        uri: the specific URI of the request
        protocol: HTTP/HTTPS protocol to be used (based on config)
        host: host address
        api_ver: the current api ver
        data: The request body to be sent
        headers: X-road headers

    Returns: A Rest object with all the properties in the api_tests response to proceed
    """
    url = f"{protocol}://{host}/{api_ver}{uri}"

    try:
        logger.debug(f"URL: {url} created and now sending the {req_method} request to the server {host}")
        # If there are headers but there's no key specifying the content type
        resp = re.request(req_method, url=url, json=data, headers=headers, timeout=120)
        return resp

    except re.exceptions.RequestException as ex:
        logger.error(f"Unknown exception occurred. Please check the logs for the details. \n {ex}")


# ----------------------------------------------- Helpers --------------------------------------------------------#
#                                                                                                                 #
# ----------------------------------------------------------------------------------------------------------------#

def load_valid_schema(file_name):
    """
    Loads the validation schema file
    Args:
        file_name: The name of the JSON file

    Returns: a file object
    """
    try:
        file_path = os.path.join(os.path.join(os.path.dirname(__file__), "api_tests/loan_calc_schema"), file_name)
        with open(file_path, mode="r") as schema_file:
            schema = json.loads(schema_file.read())
            return schema

    except Exception as e:
        logger.error("Failed to load JSON schema file!\n{}".format(e))


def assert_schema(resp_data, schema_file_name="calculate_resp_valid.json"):
    """
    Asserts that the input schema is according the loaded JSON schema
    Args:
        resp_data: The JSON of the API response
        schema_file_name: Pre-Defined schema file name

    Returns: True
    """
    valid_schema = load_valid_schema(file_name=schema_file_name)
    return validate(resp_data, schema=valid_schema)


def gen_rand_int(min_length, max_length) -> int:
    """
    Generates a random ID to be used for creating a user
    Args:
        min_length: Min length of the integer
        max_length: Max length of the integer
    Returns: An int value
    """
    rand_int = random.randrange(min_length, max_length)
    logger.debug(f"Generated random integer: {rand_int} with {len(str(rand_int))} chars")
    return rand_int


def gen_rand_str(length) -> str:
    """
    Generates a random str to be used for creating a user
    Args:
        length: Max length of str

    Returns: A str value
    """
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=length))
    logger.debug(f"Generated random string: {rand_str} with {len(rand_str)} chars")
    return rand_str


def invalid_req_methods(req_method, uri):
    """
    Sends the API requests using incorrect methods
    Args:
        req_method:
        uri:

    Returns:

    """
    resp_invalid_methods = request_operation(req_method=req_method, uri=uri, protocol=cl.api_web_protocol, host=cl.api_web_host,
                                             data=None, api_ver=cl.api_ver, headers=cl.headers)
    return resp_invalid_methods


# ----------------------------------------- Calculator Specific --------------------------------------------------#
#                                                                                                                 #
# ----------------------------------------------------------------------------------------------------------------#
def calculate_loan(uri=cl.calc_uri, period=120, prod="LOANSE02", amount=85000, interest=10.95, repay_day=27,
                   admin_fee=40, concl_fee=695, currency="SEK"):
    """
    Sends a req to the /calculate endpoint to create loan repayment details for the specified period and amount
    Args:
        uri: The URI for the loan endpoint
        period: The amount for which loan will be borrowed
        prod: The type of Product e.g. Loan program
        amount: The amount of Loan
        interest: The annual interest rate
        repay_day: Day on which the loan will be repaid
        admin_fee: The administration fee for the loan processing - added monthly
        concl_fee: The one time loan conclusion fee
        currency: The currency in which loan is required

    Returns: The loan repayment details and the resp object
    """
    loan_req_body = {
        "maturity": period,
        "productType": prod,
        "amount": amount,
        "interestRate": interest,
        "monthlyPaymentDay": repay_day,
        "administrationFee": admin_fee,
        "conclusionFee": concl_fee,
        "currency": currency
    }
    logger.debug("Sending the req to fetch loan repayment details with the following req body: {}".format(loan_req_body))
    loan_details_resp = post_req(uri=uri, protocol=cl.api_web_protocol, host=cl.api_web_host,
                                 headers=cl.headers, data=loan_req_body, api_ver=cl.api_ver)

    logger.debug("Loan repayment details created successfully!")
    return loan_details_resp
