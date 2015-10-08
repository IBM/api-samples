#!/usr/bin/env python3
# This sample demonstrates how to use the tenant_management endpoint in the
# REST API.

# For this scenario to work there must already be tenants on the system the
# sample is being run against. Tenant id 1 must exist.
# The scenario demonstrates the following actions:
#  - How to get tenants.
#  - How to filter the data using tenant_id.

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import json
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():

    # First we have to create our client
    client = client_module.RestApiClient(version='5.0')

    # -------------------------------------------------------------------------
    # Basic 'GET'
    # In this example we'll be using the GET endpoint of
    # config/access/tenant_management/tenants without
    # any parameters. This will print absolutely everything it can find, every
    # parameter of every tenant.

    # Send in the request
    SampleUtilities.pretty_print_request(
          client,
          'config/access/tenant_management/tenants',
          'GET')
    response = client.call_api('config/access/tenant_management/tenants',
                               'GET')

    # Check if the success code was returned to ensure the call to the API was
    # successful.
    if response.code != 200:
        print('Failed to retrieve the list of tenants')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # Since the previous call had no parameters and response has a lot of text,
    # we'll just print out the number of tenants
    response_body = json.loads(response.read().decode('utf-8'))
    print('Number of tenants retrived: ' + str(len(response_body)))

    # -------------------------------------------------------------------------
    # Using the tenant_id parameter with 'GET'
    # Sometimes you'll want to narrow down your search to a specific tenant.
    # You can use the tenant_id parameter to carefully select what is returned.

    # Setting a variable for tenant_id
    tenant_id = '1'

    # Send in the request
    SampleUtilities.pretty_print_request(
        client, 'config/access/tenant_management/tenants/' + tenant_id,
        'GET')
    response = client.call_api(
        'config/access/tenant_management/tenants/' + tenant_id, 'GET')

    # Always check the response code
    if response.code != 200:
        print('Failed to retrieve list of tenants')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # And output the data
    SampleUtilities.pretty_print_response(response)

if __name__ == "__main__":
    main()
