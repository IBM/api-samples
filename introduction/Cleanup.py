#!/usr/bin/env python3
# This script is used to clean up data created by the sample code
# run python Cleanup.py -h for usage information.

import argparse
import os
import sys

import importlib
sys.path.append(os.path.realpath('../modules'))
client_module = importlib.import_module('RestApiClient')


def main():
    client = client_module.RestApiClient(version='5.0')
    cleanup_introduction_data(client)
    cleanup_06_common_parameters(client)


# This function tears down data used in the introduction samples.
def cleanup_introduction_data(client):
    response = client.call_api('reference_data/sets/rest_api_samples_testset',
                               'DELETE')
    print(response.code)
    print("Sample data removed")


# This function tears down data used in the 06_CommonParameters sample
def cleanup_06_common_parameters(client):
    response = client.call_api(
        'reference_data/sets/rest_api_samples_authorized_users', 'DELETE')
    print(response.code)
    response = client.call_api(
        'reference_data/sets/rest_api_samples_authorized_ips', 'DELETE')
    print(response.code)
    response = client.call_api(
        'reference_data/sets/rest_api_samples_keywords', 'DELETE')
    print(response.code)
    response = client.call_api(
        'reference_data/sets/rest_api_samples_authorized_ports', 'DELETE')
    print(response.code)
    response = client.call_api(
        'reference_data/sets/rest_api_samples_recent_access', 'DELETE')
    print(response.code)
    print("Sample data for 06_CommonParameters removed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup sample data")
    parser.add_argument(
        'script', default='all', nargs='?',
        help='The name of the script you would like to clean up after',
        choices=['02_QueryParameters.py', '03_PathParameters.py',
                 '04_BodyParameters.py', '06_CommonParameters', 'all'])

    client = client_module.RestApiClient(version='5.0')
    args = parser.parse_args()
    if (args.script == '02_QueryParameters.py'):
        cleanup_introduction_data(client)
    elif (args.script == '03_PathParameters.py'):
        cleanup_introduction_data(client)
    elif (args.script == '04_BodyParameters.py'):
        cleanup_introduction_data(client)
    elif (args.script == '06_CommonParameters.py'):
        cleanup_06_common_parameters(client)
    elif (args.script == 'all'):
        main()
