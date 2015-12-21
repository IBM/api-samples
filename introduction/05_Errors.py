#!/usr/bin/env python3
# This sample demonstrates some common errors that can be made while using the
# REST API. It shows the information that is returned with an error response to
# help you diagnose the problem.

# For a list of the endpoints that you can use along with the errors that
# they might return you can view the REST API interactive help page on your
# deployment at https://<hostname>/api_doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/capabilities endpoint.

import os
import sys
import urllib

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():
    # Create our client.
    client = client_module.RestApiClient(version='5.0')

    # While using the REST API an error may occur. Information about
    # the error is returned to you in the HTTP response that you receive.
    # The HTTP code in the response can tell you a little bit about the error.
    # A code in the 400 range indicates that there was a problem with the
    # request.
    # A code in the 500 range indicates that there was a problem with the
    # server.
    # In addition to the response code, the response body contains information
    # about the error that occurred.

    # In this example we are trying to access the contents of a reference data
    # set that does not exist.
    try:
        SampleUtilities.pretty_print_request(
            client, 'reference_data/sets/rest_api_samples_does_not_exist',
            'GET')
        response = client.call_api(
            'reference_data/sets/rest_api_samples_does_not_exist', 'GET')
    except urllib.error.HTTPError as e:
        response = e

    SampleUtilities.pretty_print_response(response)

    # In this example we are passing a query parameter using the wrong name.
    try:
        SampleUtilities.pretty_print_request(
            client, 'reference_data/sets?wrong_name=fake', 'POST')
        response = client.call_api('reference_data/sets?wrong_name=fake',
                                   'POST')
    except urllib.error.HTTPError as e:
        response = e

    SampleUtilities.pretty_print_response(response)

if __name__ == "__main__":
    main()
