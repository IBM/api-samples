#!/usr/bin/env python3
# This script is used to clean up data created by the sample code
# run python Cleanup.py -h for usage information.

import argparse
import os
import sys
sys.path.append(os.path.realpath('../modules'))

from RestApiClient import RestApiClient


def main():
    client = RestApiClient(version='3.0')
    cleanup_01_sets(client)
    cleanup_02_maps(client)
    cleanup_03_map_of_sets(client)
    cleanup_04_tables(client)


# This function tears down data used in the 01_Sets sample
def cleanup_01_sets(client):
    response = client.call_api(
        'reference_data/sets/rest_api_samples_suspect_ips', 'DELETE')
    print(response.code)
    print(response.read().decode('utf-8'))
    response = client.call_api(
        'reference_data/sets/rest_api_samples_blocked_ips', 'DELETE')
    print(response.code)
    print(response.read().decode('utf-8'))
    print("Sample data for 01_Sets removed")


# This function tears down data used in the 02_Maps sample
def cleanup_02_maps(client):
    response = client.call_api(
        'reference_data/maps/rest_api_samples_current_admin_shift', 'DELETE')
    print(response.code)
    print(response.read().decode('utf-8'))
    print("Sample data for 02_Maps removed")


# This function tears down data used in the 03_MapOfSets sample
def cleanup_03_map_of_sets(client):
    response = client.call_api(
        'reference_data/map_of_sets/rest_api_samples_login_events', 'DELETE')
    print(response.code)
    print(response.read().decode('utf-8'))
    print("Sample data for 03_MapOfSets removed")


# This function tears down data used in the 04_Tables sample
def cleanup_04_tables(client):
    response = client.call_api(
        'reference_data/tables/rest_api_samples_server_access', 'DELETE')
    print(response.code)
    print(response.read().decode('utf-8'))
    print("Sample data for 04_Tables removed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup sample data")
    parser.add_argument(
        'script', default='all', nargs='?',
        help='The name of the script you would like to clean up after',
        choices=['01_Sets.py', '02_Maps.py', '03_MapOfSets.py', '04_Tables.py',
                 'all'])

    client = RestApiClient(version='3.0')
    args = parser.parse_args()
    if (args.script == '01_Sets.py'):
        cleanup_01_sets(client)
    elif (args.script == '02_Maps.py'):
        cleanup_02_maps(client)
    elif (args.script == '03_MapOfSets.py'):
        cleanup_03_map_of_sets(client)
    elif (args.script == '04_Tables.py'):
        cleanup_04_tables(client)
    elif (args.script == 'all'):
        main()
