#!/usr/bin/env python3

# In this sample you will see how the access control firewall rules of
# each server host can be retrieved and updated using the REST API.
# Access control firewall rules are the custom iptable rules defined by
# the users and are different from the default iptable rules used by the
# QRadar system. Updating the access control firewall rules won't affact
# the default rules in QRadar deployment. The example shows how to add a
# new rule to open a new port on each managed host.

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
    # In this example we'll be using the GET endpoint of system/servers without
    # any parameters. This will print all the servers in the deployment

    # Send in the request
    SampleUtilities.pretty_print_request(client, 'system/servers', 'GET')
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

        print('Get the current firewall rules.')
        endpoint = '/system/servers/' + str(server_id) + '/firewall_rules'
        SampleUtilities.pretty_print_request(client, endpoint, 'GET')
        response = client.call_api(endpoint, 'GET')

        if (response.code != 200):
            print('Failed to retrieve the firewall rules of the server ' + str(
                server_id))
            SampleUtilities.pretty_print_response(response)
            sys.exit(1)

        response_body = json.loads(response.read().decode('utf-8'))
        print(json.dumps(response_body, indent=4))

        print('Add a new firewall rule and save back to the server.')
        # Have the user input the server Id.
        ip = input(
            'Please enter the ip of the host from where to '
            + 'access the server.\n')
        port = input(
            'Please enter the port on the server you want to access.\n')
        protocol = input(
            'Please enter the protocol (TCP, UDP, ANY) used for the access.\n')
        response_body.append({
            "is_any_source_ip": True,
            "port_range": None,
            "port_type": "SINGLE",
            "protocol": protocol,
            "single_port": port,
            "source_ip": ip
        })
        headers = {}
        headers['Content-Type'] = 'application/json'
        endpoint = 'system/servers/' + str(server_id) + '/firewall_rules'
        SampleUtilities.pretty_print_request(
            client,
            endpoint,
            'PUT',
            headers=headers)
        response = client.call_api(
            endpoint,
            'PUT',
            headers=headers,
            data=json.dumps(response_body).encode())
        SampleUtilities.pretty_print_response(response)
        if (response.code != 200):
            print('Failed to update the firewall rules of the server ' + str(
                server_id))
            sys.exit(1)


if __name__ == "__main__":
    main()
