#!/usr/bin/env python3

# In this sample you will see how to manage extensions using the REST API.
# The sample contains uploading extension, installing extension, checking
# installing task and delete extension.


import json
import os
import sys
import time

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')
SampleUtilities = importlib.import_module('SampleUtilities')


def upload_extension():
    # Create our client
    client = client_module.RestApiClient(version='5.0')

    # Add Content-Type to request header
    request_header = {}
    request_header['Content-Type'] = 'application/zip'

    # setup file for posting
    cwd = os.path.dirname(os.path.realpath(__file__))
    app_zip_file_path = os.path.join(cwd, 'ExtensionPackageTest.zip')
    app_zip_file = open(app_zip_file_path, 'rb')

    data = app_zip_file.read()

    response = client.call_api('config/extension_management/extensions',
                               'POST', headers=request_header, data=data)

    # If the response code is 201, that means the extension package has been
    # successfully uploaded and the extension id will be returned.
    # Otherwise -1 will be returned and the full response body is provided with
    # error message inside.
    if (response.code != 201):
        print('Failed to upload the extension package.')
        SampleUtilities.pretty_print_response(response)
        return -1
    else:
        # Extract the extension id from the response body.
        response_body = json.loads(response.read().decode('utf-8'))
        extension_id = response_body['id']

        print('The extension has been uploaded with id = ' +
              str(extension_id))
        return extension_id


def install_extension(extension_id):
    # Create our client
    client = client_module.RestApiClient(version='5.0')

    # query parameters
    # action_type: The desired action to take on
    # the Extension (INSTALL or PREVIEW)
    # overwrite:  If true, any existing items on the importing system will be
    # overwritten if the extension contains the same items.
    # If false, existing items will be preserved,
    # and the corresponding items in the extension will be skipped.
    params = {'action_type': 'INSTALL',
              'overwrite': 'true'}

    # construct api url with path parameter.
    url = 'config/extension_management/extensions/' + str(extension_id)

    response = client.call_api(url, 'POST',  params=params)

    # Installing extension process is asynchronous. If 202 is returned,
    # that means the installing task is started and the returned status id
    # is used for tracking the asynchronous task status.
    if (response.code != 202):
        print("Failed to start installing task.")
        SampleUtilities.pretty_print_response(response)
        return -1
    else:
        response_body = json.loads(response.read().decode('utf-8'))
        status_id = response_body['status_id']
        print('The extension installing task has been started.')
        return status_id


def check_install_status(status_id):
    # Create our client
    client = client_module.RestApiClient(version='5.0')

    # construct api url with path parameter.
    url = 'config/extension_management/extensions_task_status/'+str(status_id)

    response = client.call_api(url, 'GET')

    # if there is no error, the status of installing task will be returned.
    if (response.code != 200):
        print("Failed to check installing task status.")
        SampleUtilities.pretty_print_response(response)
        status = 'FAILED'
    else:
        response_body = json.loads(response.read().decode('utf-8'))
        status = response_body['status']

    return status


def delete_installed_extension(extension_id):
    # Create our client
    client = client_module.RestApiClient(version='5.0')

    # construct api url with path parameter.
    url = 'config/extension_management/extensions/' + str(extension_id)

    response = client.call_api(url, 'DELETE')

    if (response.code == 202):
        print('The extension has been deleted.')
    else:
        print('Failed to delete the extension.')


def main():
    # upload the extension package
    extension_id = upload_extension()

    if (extension_id != -1):
        # if extension package uploaded successfully, start installing
        # extension task
        status_id = install_extension(extension_id)

        if (status_id != -1):
            # if extension installing task start wit no error, keep checking
            # the status every 5s until the it is completed or has errors or
            # time out.
            status = 'PROCESSING'

            count = 60
            while ((status == 'PROCESSING' or status == "QUEUED") and
                   count > 0):
                status = check_install_status(status_id)
                print('Installing status: ' + status)
                count = count - 1
                if ((status == 'PROCESSING' or status == "QUEUED") and
                        count == 0):
                    print('Installing process timed out.')
                    sys.exit(1)
                time.sleep(5)

            if (status == 'COMPLETED'):
                # delete the extension once it complete installed. If you want
                # to keep the extension, please comment out the line below.
                delete_installed_extension(extension_id)

        else:
            sys.exit(1)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
