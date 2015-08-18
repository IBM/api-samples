#!/usr/bin/env python3
# This sample shows how to use path parameters with the REST API.

# For a list of the endpoints that you can use along with the parameters that
# they accept you can view the REST API interactive help page on your
# deployment at https://<hostname>/api_doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/capabilities endpoint.

import os
import sys
import Cleanup

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():

    # Create our client and set up some sample data.
    client = client_module.RestApiClient(version='5.0')
    setup_data(client)

    # Some endpoints accept path parameters.
    # These parameters are inserted into the path portion of the URL at
    # specific locations. In this example we are retrieving the contents of a
    # reference set named 'rest_api_samples_testset'.
    SampleUtilities.pretty_print_request(
        client, 'reference_data/sets/rest_api_samples_testset', 'GET')
    response = client.call_api(
        'reference_data/sets/rest_api_samples_testset', 'GET')
    SampleUtilities.pretty_print_response(response)

    # Query parameters and path parameters can be combined in a single request.
    # Here we are adding a value to the reference set we just looked at.
    SampleUtilities.pretty_print_request(
        client, 'reference_data/sets/rest_api_samples_testset?value=' +
        'rest_api_sample_value', 'POST')
    response = client.call_api(
        'reference_data/sets/rest_api_samples_testset?value=' +
        'rest_api_sample_value', 'POST')

    # Along with GET requests, POST and DELETE requests often return
    # information that can be used to confirm the results of the request.
    SampleUtilities.pretty_print_response(response)

    # Now we can look at the contents of the reference set again to see the
    # value we added.
    response = client.call_api('reference_data/sets/rest_api_samples_testset',
                               'GET')
    SampleUtilities.pretty_print_response(response)

    # You can uncomment this line to have this script remove the data it
    # creates after it is done, or you can invoke the Cleanup script directly.
    # Cleanup.cleanup_introduction_data(client)


# This helper function sets up data used in this sample.
def setup_data(client):
    SampleUtilities.data_setup(
        client, 'reference_data/sets?name=rest_api_samples_testset&' +
        'element_type=ALN', 'POST')

if __name__ == "__main__":
    main()
