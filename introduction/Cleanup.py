# This script is used to clean up data created by the sample code
# run python Cleanup.py -h for usage information.

import sys, os
sys.path.append(os.path.realpath('../modules'))
import argparse

from RestApiClient import RestApiClient
import SampleUtilities

def main():
    client = RestApiClient()
    cleanup_introduction_data(client)

# This function tears down data used in the 02_QueryParameters sample.
def cleanup_introduction_data(client):
    response = client.call_api('referencedata/sets/rest_api_samples_testset', 'DELETE')
    print(response.code)
    print(response.read().decode('utf-8'))
    print("Sample data removed")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup sample data")
    parser.add_argument('script', default='all', nargs='?', help='The name of the script you would like to clean up after',
                        choices=['02_QueryParameters.py', '03_PathParameters.py', '04_BodyParameters.py', 'all'])
    
    client = RestApiClient()    
    args = parser.parse_args()
    if (args.script == '02_QueryParameters.py'):
        cleanup_introduction_data(client)
    elif (args.script == '03_PathParameters.py'):
        cleanup_introduction_data(client)
    elif (args.script == '04_BodyParameters.py'):
        cleanup_introduction_data(client)
    elif (args.script == 'all'):
        main()
