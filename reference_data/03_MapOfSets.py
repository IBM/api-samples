# In this example we will see how data in reference maps of sets can be
# manipulated using the REST API.

# Our company is an E-retailer serving customers around the world. We have a
# number of authentication servers that allow our customers to log in securely
# to our site. The CIO of our company believes that as our business is growing
# these servers are becoming a bottleneck. He wants to monitor the activity on
# these servers in real time through the digital dashboard of his executive
# support system.

# You have already created a rule on our system that captures login events on
# the company's authentication servers and adds information about the login to
# a reference data map of sets. The map uses the IP addresses of the servers as
# keys, and stores the usernames that log in through those servers in the sets.

# For a list of the endpoints that you can use along with the parameters that
# they accept you can view the REST API interactive help page on your
# deployment at https://<hostname>/api_doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/capabilities endpoint.

import json
import os
import sys
import time
sys.path.append(os.path.realpath('../modules'))

from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities


def main():
    # Create our client and set up some sample data.
    client = RestApiClient()
    setup_data(client)

    # Here we have a look at the data in this map of sets.
    response = client.call_api('reference_data/map_of_sets/rest_api_samples_login_events', 'GET')
    SampleUtilities.pretty_print_response(response)

    # Retrieve the map of sets and load it into a JSON object.
    response = client.call_api('reference_data/map_of_sets/rest_api_samples_login_events', 'GET')
    response_body = json.loads(response.read().decode('utf-8'))

    # Capture the data portion of the map of sets.
    data = response_body['data']

    # Also get the current time so that the CIO's dashboard can plot the results
    # over time.
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')

    # We now empty the reference map of sets so that new data can start to
    # accumulate. We empty it now so that we don't miss new events if we have a
    # lot of data to process. Note that by using the purgeOnly parameter we are
    # only emptying the collection, not deleting it.
    print("Purging the collection so that new data can be collected.")
    response = client.call_api('reference_data/map_of_sets/rest_api_samples_login_events?purge_only=true', 'DELETE')
    SampleUtilities.pretty_print_response(response)

    # Go through the data, find the information we are interested in, and send
    # it to the CIO's dashboard.
    for key in data.keys():
        number_of_elements = len(data[key])
        send_data_to_dashboard(current_time, key, number_of_elements)

    # You can uncomment this line to have this script remove the data it
    # creates after it is done, or you can invoke the Cleanup script directly.
    # Cleanup.cleanup_02_map_of_sets(client)


# This helper function sets up data used in this sample.
def setup_data(client):
    SampleUtilities.data_setup(client, 'reference_data/map_of_sets?name=rest_api_samples_login_events&element_type=ALN', 'POST')

    SampleUtilities.data_setup(client, 'reference_data/map_of_sets/rest_api_samples_login_events?key=3.4.5.6&value=bob', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/map_of_sets/rest_api_samples_login_events?key=3.4.5.6&value=frank', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/map_of_sets/rest_api_samples_login_events?key=3.4.5.6&value=jane', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/map_of_sets/rest_api_samples_login_events?key=2.12.42.7&value=kim', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/map_of_sets/rest_api_samples_login_events?key=2.12.42.7&value=serge', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/map_of_sets/rest_api_samples_login_events?key=2.12.42.7&value=sue', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/map_of_sets/rest_api_samples_login_events?key=2.12.42.7&value=rick', 'POST')


# This function simulates sending the information we gather to the the CIO's
# digital dashboard.
def send_data_to_dashboard(time, ip_address, number_of_logins):
    print('At ' + time + '  ' + str(number_of_logins) + ' users had logged in to ' + ip_address + ' since we last checked.')


if __name__ == "__main__":
    main()
