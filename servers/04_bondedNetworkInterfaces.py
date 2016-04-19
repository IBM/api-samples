#!/usr/bin/env python3

# In this sample you will see how to create a bonded network interface on top
# of the existing ethernet interfaces, change the settings of the bonded
# network interface and unbond it to recover the slave interfaces back to
# normal ethernet interfaces using REST API.

import json
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def inputSettings():
    ifaces = None
    while (ifaces is None or len(ifaces) == 0):
        ifaces = input(
            'Please enter the names (separated by comma) of the ethernet ' +
            'interfaces to be bonded.\n')     

    slaves = ifaces.split(sep=",")
    slavesArray = []
    for slave in slaves:
        slavesArray.append({"device_name": slave})

    # Have the user input the settings.
    role = input(
        'Please enter the role (regular, monitor or disabled) ' + 
        'of the bonded network interface.\n')
    ipversion = None
    ip = None
    mask = None
    isAutoIP = "N"
    ipversion = input('Please enter the version (ipv4 or ipv6) ' + 
                      'of the IP.\n')
    if (role == "regular"):

        if (ipversion == "ipv4"):
            ip = input('Please enter the IP.\n')
            mask = input('Please enter the netmask.\n')
        else:
            isAutoIP = input(
                'Do you want the IP to be automatically assigned (Y/N)? ')
            if (isAutoIP != "Y"):
                ip = input('Please enter the IP.\n')
    bondOpts = input('Please enter the bonding option.\n')

    ifaceObj = {"role": role, "ipversion": ipversion,
                "ip": ip, "mask": mask,
                "is_auto_ip": isAutoIP == "Y",
                "bonding_opts": bondOpts,
                "slaves": slavesArray}
    print("The settings are:")
    print(json.dumps(ifaceObj))
    return ifaceObj


def main():

    # First we have to create our client
    client = client_module.RestApiClient(version='6.0')

    # Have the user input the server Id.
    server_Id = input(
        'Please enter the Id of the server. The Id needs to be an integer. ' + 
        'The server should have some ethernet interfaces that are used for ' + 
        'the management interface or the HA crossover interface to proceed ' + 
        'this example. \n')

    # Get the existing ethernet interfaces that are available to be boned on
    # the server. We use filter to get the interfaces with role in regular,
    # monitor or disabled as they can be used for bonding.
    print('Getting the available ethernet network interfaces to be bonded on ' 
          + 'the server.')
    params = {'fields': 'device_name',
              'filter': '(role=regular) or (role=monitor) or (role=disabled)'}
    endpoint = 'system/servers/' + \
        str(server_Id) + '/network_interfaces/ethernet'
    SampleUtilities.pretty_print_request(client, endpoint, 'GET')
    response = client.call_api(endpoint, 'GET', params=params)
    response_body = json.loads(response.read().decode('utf-8'))
    if len(response_body) == 0:
        print('There is no ethernet network interfaces that can be used to ' + 
              'create bonded network interface on the server. Exit. ')
        sys.exit(1)
    print('Available ethernet interfaces to be bonded:')
    for eth in response_body:
        print(eth['device_name'])

    # Have the user input the settings of the bonded interface to be created.
    ifaceObj = inputSettings()

    # Create the bonded interface
    headers = {}
    headers['Content-Type'] = 'application/json'
    endpoint = 'system/servers/' + \
        str(server_Id) + '/network_interfaces/bonded'
    SampleUtilities.pretty_print_request(
        client, endpoint, 'POST', headers=headers)
    response = client.call_api(
        endpoint, 'POST', headers=headers, data=json.dumps(ifaceObj).encode())

    # Check if the success code was returned to ensure the call to the API was
    # successful.
    iface = None
    if (response.code != 201):
        print('Failed to create the bonded network interface')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)
    else:
        response_body = json.loads(response.read().decode('utf-8'))
        iface = response_body['device_name']
        print('Successfully created the bonded network interface ' + iface)

    # update the settings
    proceed = input(
        'Continue running this sample will guide you to change the  ' + 
        'settings of the bonded network interface. ' + 
        'Are your sure to continue (Y/N)? ')

    if (proceed != 'Y'):
        sys.exit(1)

    # Have the user input the new settings.
    ifaceObj = inputSettings()

    # update the settings
    headers = {}
    headers['Content-Type'] = 'application/json'
    endpoint = 'system/servers/' + \
        str(server_Id) + '/network_interfaces/bonded/' + iface
    SampleUtilities.pretty_print_request(
        client, endpoint, 'POST', headers=headers)
    response = client.call_api(
        endpoint, 'POST', headers=headers, data=json.dumps(ifaceObj).encode())
    if (response.code != 200):
        print('Failed to update the bonded network interface ' + iface)
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)
    else:
        print(iface + ' is successfully updated\n')

    # unbond the bonded interface
    proceed = input(
        'Continue running this sample will guide you to unbond the  ' + 
        'newly created bonded network interface and recover its slave ' + 
        'interfaces to ethernet interfaces. ' + 
        'Are your sure to continue (Y/N)? ')

    if (proceed != 'Y'):
        sys.exit(1)

    # Accept header for DELETE endpoints.
    headers = {'Accept': 'text/plain'}
    endpoint = 'system/servers/' + \
        str(server_Id) + '/network_interfaces/bonded/' + iface
    SampleUtilities.pretty_print_request(
        client, endpoint, 'DELETE', headers=headers)
    response = client.call_api(
        endpoint, 'DELETE', headers=headers)
    # Verify that DELETE was successful.
    if response.code != 200:
        print('Failed to delete the bonded interface ' + iface)
        SampleUtilities.pretty_print_response(response)
        exit(1)
    else:
        print(iface + ' is successfully deleted\n')

if __name__ == "__main__":
    main()
