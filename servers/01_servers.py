#!/usr/bin/env python3

# In this sample you will see how to retrieve a list of the server hosts in the
# QRadar deployment and how the settings of each server hosts can be retrieved
# and updated using the REST API.
# Currently, we only support updating the email server address of a server
# through the endpoint.

import json
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():

    # First we have to create our client
    client = client_module.RestApiClient(version='6.0')

    # -------------------------------------------------------------------------
    # Basic 'GET'
    # In this example we'll be using the GET endpoint of system/servers without
    # any parameters. This will print all the servers in the deployment

    # Send in the request
    SampleUtilities.pretty_print_request(client,
                                         'system/servers',
                                         'GET')
    response = client.call_api('system/servers', 'GET')

    # Check if the success code was returned to ensure the call to the API was
    # successful.
    if (response.code != 200):
        print('Failed to retrieve the list of servers')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # loop through the servers
    response_body = json.loads(response.read().decode('utf-8'))
    print('Number of servers retrieved: ' + str(len(response_body)))

    for server in response_body:
        server_id = server['server_id']
        print('server_id={0}'.format(server_id))

        endpoint = '/system/servers/' + str(server_id)
        SampleUtilities.pretty_print_request(client, endpoint, 'GET')

        response = client.call_api(endpoint, 'GET')

        if (response.code != 200):
            print('Failed to retrieve the details of server ' + str(server_id))
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)

        response_body = json.loads(response.read().decode('utf-8'))
        print('email server address = ' +
              response_body['email_server_address'])

        # update the email server address to the same value
        headers = {}
        headers['Content-Type'] = 'application/json'
        endpoint = 'system/servers/' + str(server_id)
        SampleUtilities.pretty_print_request(
            client, endpoint, 'POST', headers=headers)
        data = {"email_server_address": response_body['email_server_address']}
        response = client.call_api(endpoint, 'POST',
                                   headers=headers,
                                   data=json.dumps(data).encode())

        if (response.code != 200):
            print('Failed to update the details of server ' + str(server_id))
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)

if __name__ == "__main__":
    main()
