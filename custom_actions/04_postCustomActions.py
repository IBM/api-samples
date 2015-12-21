#!/usr/bin/env python3
# This sample demonstrates how to use various POST /custom_actions/ endpoints
# available REST API.
#
# WARNING: This sample makes changes to the QRadar system and it is
# recommended that it is not run against a production system.
#
# This script can be run once as custom actions require their names
# to be unique.
# Users can edit the assigned names in this script to enable
# multiple executions.
#
# The scenario demonstrates the following actions:
#  - How to post custom action scripts to the system.
#  - How to update existing scripts on the system.
#  - How to post custom actions to the system.
#  - How to update existing custom actions on the system.

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.
import json
import sys
import os

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def main():
    # Create our client.
    rest_client = client_module.RestApiClient(version='5.0')
    # Endpoints used in this sample
    scripts_endpoint = 'analytics/custom_actions/scripts'
    actions_endpoint = 'analytics/custom_actions/actions'
    # Variable to hold the root path to the custom actions sample folder
    root_path = os.path.dirname(os.path.realpath(__file__))
    # Script file name & path to where it is stored
    file_name = 'python_sample.py'
    file_path = os.path.join(root_path, 'custom_action_samples', file_name)

    # Opening script file in local file system
    with open(file_path) as script:
        # Adding a request header to contain the file name
        # Also setting content-type header to application/octet-stream
        request_header = rest_client.headers.copy()
        request_header['file_name'] = file_name
        request_header['Content-Type'] = 'application/octet-stream'
        # Reading the content of the script file & encoding it for use
        # with the endpoint.
        script_data = script.read()
        script_data_encoded = str.encode(script_data)

    SampleUtilities.pretty_print_request(rest_client,
                                         scripts_endpoint,
                                         'POST')
    # Calling scripts endpoint to POST script file.
    response = rest_client.call_api(scripts_endpoint,
                                    'POST',
                                    headers=request_header,
                                    data=script_data_encoded)
    # Checking for a successful response code.
    if response.code != 201:
        print('Failed to POST custom action script to the server')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    script_response = json.loads(response.read().decode('utf-8'))
    retrieved_id = str(script_response['id'])
    retrieved_name = str(script_response['file_name'])

    format_str = 'Script successfully uploaded. Values returned: id=[{0}],'\
                 ' file name=[{1}].\n'

    print(format_str.format(retrieved_id, retrieved_name))

    print("Demonstrating updating scripts via /scripts/{id} endpoint...")
    # This script id will be used with the POST /scripts/{id} endpoint
    # and with the POST /actions endpoint.
    script_id = script_response['id']

    # Demonstrating updating an existing script resource
    file_name = 'bash_sample.sh'
    file_path = os.path.join(root_path, 'custom_action_samples', file_name)

    with open(file_path) as script:
        # Adding a request header to contain the file name
        # Also setting content-type header to application/octet-stream
        request_header = rest_client.headers.copy()
        request_header['file_name'] = file_name
        request_header['Content-Type'] = 'application/octet-stream'
        # Reading the content of the script file & encoding it
        # for use with the endpoint.
        script_data = script.read()
        script_data_encoded = str.encode(script_data)
    # Updating endpoint to include /{id}.
    scripts_endpoint += '/' + str(script_id)
    SampleUtilities.pretty_print_request(rest_client,
                                         scripts_endpoint,
                                         'POST')
    # Calling the POST /scripts/{id} endpoint to
    # update the script resource.
    response = rest_client.call_api(scripts_endpoint,
                                    'POST',
                                    headers=request_header,
                                    data=script_data_encoded)

    if (response.code != 200):
        print('Failed to POST updated custom action script to the server')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)
    # Extracting script id and file name from the response.
    script_response = json.loads(response.read().decode('utf-8'))
    retrieved_id = str(script_response['id'])
    retrieved_name = str(script_response['file_name'])

    format_str = 'Script successfully updated. Values returned: id=[{0}],'\
                 ' file name=[{1}].\n'

    print(format_str.format(retrieved_id, retrieved_name))

    # Using the script ID generated by the previous calls we can
    # now create a new custom action.
    # Custom actions are posted to the server as a complete object.
    # This is demonstrated below.

    # Dict object to contain the custom action
    custom_action = {}
    custom_action['name'] = "Custom Action Demonstration"
    custom_action['description'] = "Demonstrating POST custom action endpoint"
    # GET /interpreters can be used to return a collection of available
    # interpreters from which ids can be retrieved. But for demo purposes
    # this has been hard coded here to 1.
    custom_action['interpreter'] = 1
    # ID of script created earlier
    custom_action['script'] = script_id
    # Custom Action parameters are stored within a list object
    custom_action_params = []
    # Param dict objects to house each custom action parameter
    param1 = {}
    param1['name'] = 'demoParam1'
    # Must be either 'fixed', or 'dynamic'.
    param1['parameter_type'] = 'fixed'
    # Only fixed parameters will can be encrypted.
    # This will encrypt the value of the parameter at storage time
    param1['encrypted'] = True
    param1['value'] = 'Hello World!'

    param2 = {}
    param2['name'] = 'demoParam2'
    # The value of dynamic parameters will be replaced with the action value
    # occurring in the event which triggers
    # the rule containing the custom action
    param2['parameter_type'] = 'dynamic'
    # Dynamic parameters cannot be encrypted, if set to
    # true it will be defaulted back to false
    param2['encrypted'] = False
    # This value will be replaced with the actual source IP of the event
    # which triggered the rule containing the custom action.
    # Available dynamic parameter values can be retrieved via the
    # /api/ariel/databases/events?fields=columns(name) endpoint.
    param2['value'] = 'sourceip'

    custom_action_params.append(param1)
    custom_action_params.append(param2)

    # Adding custom action parameters to custom action
    custom_action['parameters'] = custom_action_params

    # Converting custom action object to json and
    # encoding it for use with the endpoint.
    custom_action = json.dumps(custom_action).encode()

    action_headers = rest_client.headers.copy()
    action_headers['Content-Type'] = 'application/json'

    SampleUtilities.pretty_print_request(rest_client,
                                         actions_endpoint,
                                         'POST')
    response = rest_client.call_api(actions_endpoint,
                                    'POST',
                                    headers=action_headers,
                                    data=custom_action)

    if (response.code != 201):
        print('Failed to POST custom action to the server')
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    # The created custom action is returned, which will
    # have it's ID within a new field.
    action_response = json.loads(response.read().decode('utf-8'))
    action_id = action_response['id']

    print("Successfully posted custom action [returned id=" +
          str(action_id) + "].")

    action_name = str(action_response['name'])
    action_desc = str(action_response['description'])
    action_interpreter = str(action_response['interpreter'])
    action_script = str(action_response['script'])

    format_str = 'Custom action values:\n[name={0}'\
                 ', description={1} '\
                 ', interpreter={2}'\
                 ', script={3}].'

    print(format_str.format(action_name,
                            action_desc,
                            action_interpreter,
                            action_script))

    print("Parameters: ")
    for each in action_response['parameters']:

        param_name = str(each['name'])
        param_type = str(each['parameter_type'])
        param_encrypted = str(each['encrypted'])
        param_value = str(each['value'])

        format_str = '[name={0}'\
                     ', parameter_type={1}'\
                     ', encrypted={2}'\
                     ', value={3}].'

        print(format_str.format(param_name,
                                param_type,
                                param_encrypted,
                                param_value))

    print()

    # Demonstrating the POST /actions/{id} endpoint used
    # for updating custom actions

    updated_action = {}
    updated_action['id'] = action_id
    updated_action['name'] = 'Updated Demo Custom Action'
    # Interpreter & script required even
    # if they remain unchanged.
    updated_action['interpreter'] = 2
    updated_action['script'] = script_id
    # Replacing old params with a single new parameter.
    updated_action['parameters'] = [{'name': 'demoParam',
                                     'parameter_type': 'fixed',
                                     'encrypted': False,
                                     'value': 'new param'}]

    updated_action = json.dumps(updated_action).encode()
    # Appending endpoint with action id.
    actions_endpoint += '/' + str(action_id)

    SampleUtilities.pretty_print_request(rest_client,
                                         actions_endpoint,
                                         'POST')
    response = rest_client.call_api(actions_endpoint,
                                    'POST',
                                    headers=action_headers,
                                    data=updated_action)

    if (response.code != 200):
        print('Failed to POST custom action [' +
              str(action_id) + "] to the server.")
        SampleUtilities.pretty_print_response(response)
        sys.exit(1)

    updated_response = json.loads(response.read().decode('utf-8'))

    print("Successfully posted updated custom action [" +
          str(action_id) + "] to the server")

    action_name = str(updated_response['name'])
    action_desc = str(updated_response['description'])
    action_interpreter = str(updated_response['interpreter'])
    action_script = str(updated_response['script'])

    format_str = 'Updated custom action values:\n [name={0}'\
                 ', description={1} '\
                 ', interpreter={2}'\
                 ', script={3}].'

    print(format_str.format(action_name,
                            action_desc,
                            action_interpreter,
                            action_script))

    print("Parameters: ")
    for each in updated_response['parameters']:

        param_name = str(each['name'])
        param_type = str(each['parameter_type'])
        param_encrypted = str(each['encrypted'])
        param_value = str(each['value'])

        format_str = '[name={0}'\
                     ', parameter_type={1}'\
                     ', encrypted={2}'\
                     ', value={3}].'

        print(format_str.format(param_name,
                                param_type,
                                param_encrypted,
                                param_value))

        print()
if __name__ == '__main__':
    main()
