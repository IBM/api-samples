#!/usr/bin/env python3
# This sample demonstrates how to use the tenant_management endpoint in the
# REST API.

# The scenario demonstrates the following actions:

#  - How to create tenants.
#  - How to update tenants.
#  - How to delete tenants.

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

    # You must make sure that you set the content type correctly to a type
    # accepted by the endpoint.
    headers = client.get_headers().copy()
    headers['Content-type'] = 'application/json'

    # -------------------------------------------------------------------------
    # Basic 'POST'
    # In this example we'll be using the POST endpoint of
    # config/access/tenant_management/tenants
    # This will allow us to create a new tenant.

    # Create the tenant parameter.
    body = {'name': 'Tenant_API',
            'event_rate_limit': 500,
            'flow_rate_limit': 1000,
            'description': 'This is a test!'}

    json_body = json.dumps(body).encode('utf8')
    # Send in the request
    SampleUtilities.pretty_print_request(
          client,
          'config/access/tenant_management/tenants',
          'POST',
          headers=headers)

    response = client.call_api('config/access/tenant_management/tenants',
                               'POST',
                               headers=headers,
                               data=json_body)

    # Check if the success code was returned to ensure the call to the API was
    # successful.
    if response.code != 201:
        print('Failed to create the new tenant')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # And output the new tenant id
    response_body = json.loads(response.read().decode('utf-8'))
    tenant_id = str(response_body['id'])
    print('The new tenant id: ' + tenant_id)

    # In this example we'll be using the POST endpoint of
    # config/access/tenant_management/tenants
    # This will allow us to update the new tenant
    # changing "Tenant-API" name to "Tenant-API-new".
    # Create the tenant parameter.
    body = {'name': 'Tenant_API_new',
            'event_rate_limit': 501,
            'flow_rate_limit': 1001,
            'description': 'This is a test!'}

    json_body = json.dumps(body).encode('utf8')

    # Send in the request
    SampleUtilities.pretty_print_request(
          client,
          'config/access/tenant_management/tenants/' + tenant_id,
          'POST',
          headers=headers)

    response = client.call_api(
                  'config/access/tenant_management/tenants/' + tenant_id,
                  'POST',
                  headers=headers,
                  data=json_body)

    # Check if the success code was returned to ensure the call to the API was
    # successful.
    if response.code != 200:
        print('Failed to create the new tenant')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # And output the data
    SampleUtilities.pretty_print_response(response)

    # In this example we'll be using the DELETE endpoint of
    # config/access/tenant_management/tenants
    # This will allow us to soft delete the new tenant - Tenant-API.
    # Send in the request
    SampleUtilities.pretty_print_request(
          client,
          'config/access/tenant_management/tenants/' + tenant_id,
          'DELETE')

    response = client.call_api(
        'config/access/tenant_management/tenants/' + tenant_id, 'DELETE')

    # Always check the response code
    if response.code != 200:
        print('Failed to retrieve list of tenants')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # And output the data
    SampleUtilities.pretty_print_response(response)

if __name__ == "__main__":
    main()
