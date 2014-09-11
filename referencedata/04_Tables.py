# In this example we will see how data in reference tables can be manipulated
# using the REST API.

# Our company has a multilevel security authorization architecture. Users
# are assigned an authorization server that they must use to log in to the
# network. Once inside the general network, some users are authorized to access
# the secure network. They use a different authorization server and must
# connect through an assigned port.
# We have set up a reference table that stores the ip addresses of the server
# that each user must use to login to the network. It also stores the ip
# address and port of the secure server that authorized users must use to
# connect to the secure network. We also store the time the user last logged in
# to the secure server. Rules are in place to generate offenses if users attempt
# to access the network in an unauthorized manner.

# We would like to impose a business rule to revoke a user's secure access if
# they do not log in for a period of time. This time period is determined by
# an external system.
# We would also like to generate a report showing the users that have secure
# access, those that used to have it, but let it expire, and those that don't
# have secure access, in order to track who is using our networks.

# For a list of the endpoints that you can use along with the parameters that
# they accept you can view the REST API interactive help page on your
# deployment at https://<hostname>/api_doc
# You can also retrieve a list of available endpoints through the API itself
# at the /api/help/capabilities endpoint.


import json
import os
import sys
import time
import urllib.parse
import Cleanup

sys.path.append(os.path.realpath('../modules'))
from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities


def main():
    # Create our client and set up some sample data.
    client = RestApiClient()
    setup_data(client)

    # First lets have a look at the data in the system.
    response = client.call_api('reference_data/tables/rest_api_samples_server_access', 'GET')
    SampleUtilities.pretty_print_response(response)

    response = client.call_api('reference_data/tables/rest_api_samples_server_access', 'GET')
    response_body = json.loads(response.read().decode('utf-8'))
    data = response_body['data']

    # Note that tables are stored sparsely, that is to say if a particular
    # cell is empty it does not exist in the table. However, our external
    # reporting tool can put appropriate defaults for these cells into the
    # report.
    print_custom_report(data)

    # Now our external system calculates which users should have their secure
    # access revoked.
    threshold = get_old_data_threshold(data)

    # check to see which users should have their secure access expired.
    for user in data:
        if ('Last_Secure_Login' in data[user]):
            if (data[user]['Last_Secure_Login']['last_seen'] < threshold):
                print ("User '" + user + "' has not logged in to the secure server recently. Revoking their access.")
                outer_key = user
                if ('Authorization_Server_IP_Secure' in data[user]):
                    inner_key = 'Authorization_Server_IP_Secure'
                    value = data[user]['Authorization_Server_IP_Secure']['value']
                    response = client.call_api('reference_data/tables/rest_api_samples_server_access/' + outer_key + '/' + inner_key + '?value=' + value, 'DELETE')
                if ('Authorization_Server_PORT_Secure' in data[user]):
                    inner_key = 'Authorization_Server_PORT_Secure'
                    value = data[user]['Authorization_Server_PORT_Secure']['value']
                    response = client.call_api('reference_data/tables/rest_api_samples_server_access/' + outer_key + '/' + inner_key + '?value=' + value, 'DELETE')


    # now lets have a look at the data after we updated the table.
    response = client.call_api('reference_data/tables/rest_api_samples_server_access', 'GET')
    SampleUtilities.pretty_print_response(response)

    response = client.call_api('reference_data/tables/rest_api_samples_server_access', 'GET')
    response_body = json.loads(response.read().decode('utf-8'))
    data = response_body['data']

    print_custom_report(data)


    # You can uncomment this line to have this script remove the data it
    # creates after it is done, or you can invoke the Cleanup script directly.
    # Cleanup.cleanup_04_tables(client)


# This helper function sets up data used in this sample.
def setup_data(client):
    current_time = int(time.time() * 1000)

    key_name_types = urllib.parse.quote("[{\"element_type\": \"IP\", \"key_name\": \"Authorization_Server_IP_Secure\"}, {\"element_type\": \"PORT\", \"key_name\": \"Authorization_Server_PORT_Secure\"}, {\"element_type\": \"DATE\", \"key_name\": \"Last_Secure_Login\"}, {\"element_type\": \"IP\", \"key_name\": \"Authorization_Server_IP_General\"}]")
    SampleUtilities.data_setup(client, 'reference_data/tables?name=rest_api_samples_server_access&element_type=ALN&key_name_types=' + key_name_types, 'POST')

    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=calvin&inner_key=Authorization_Server_IP_Secure&value=6.3.9.12', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=calvin&inner_key=Authorization_Server_PORT_Secure&value=443', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=calvin&inner_key=Authorization_Server_IP_General&value=7.12.15.12', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=calvin&inner_key=Last_Secure_Login&value=' + str(current_time), 'POST')

    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=socrates&inner_key=Authorization_Server_IP_General&value=7.12.14.85', 'POST')
    time.sleep(1)

    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=mill&inner_key=Authorization_Server_IP_Secure&value=6.3.9.12', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=mill&inner_key=Authorization_Server_PORT_Secure&value=443', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=mill&inner_key=Last_Secure_Login&value=' + str(current_time), 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=mill&inner_key=Authorization_Server_IP_General&value=7.13.22.85', 'POST')

    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=hobbes&inner_key=Authorization_Server_IP_Secure&value=6.3.9.12', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=hobbes&inner_key=Authorization_Server_PORT_Secure&value=22', 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=hobbes&inner_key=Last_Secure_Login&value=' + str(current_time), 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=hobbes&inner_key=Authorization_Server_IP_General&value=7.12.19.125', 'POST')

    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=aquinas&inner_key=Last_Secure_Login&value=' + str(current_time - 1000000), 'POST')
    SampleUtilities.data_setup(client, 'reference_data/tables/rest_api_samples_server_access?outer_key=aquinas&inner_key=Authorization_Server_IP_General&value=7.12.15.12', 'POST')


# This function represents work done by an external system to determine which
# users should have their secure access revoked.
def get_old_data_threshold(data):
    total_time = 0
    counter = 0
    for outer_key in data:
        for inner_key in data[outer_key]:
            if(('Authorization_Server_IP_Secure' in data[outer_key]) and ('Last_Secure_Login' in data[outer_key])):
                total_time += data[outer_key]['Last_Secure_Login']['last_seen']
                counter += 1

    return total_time / counter


# This function represents work done by an external reporting tool.
def print_custom_report(data):

    # print the table headers.
    usernames = data.keys()
    table_headers_dict = {}
    table_headers = []
    known_headers = ['Authorization_Server_IP_Secure', 'Authorization_Server_PORT_Secure', 'Authorization_Server_IP_General', 'Last_Secure_Login']

    # calculate the full list table headers, since not all columns will exist
    # in each row.
    for user in usernames:
        for header in data[user]:
            table_headers_dict[header] = ""

    # Get the table headers into a list and sort them.
    for header in table_headers_dict:
        table_headers.append(header)
    table_headers.sort()

    # pretty print the table headers.
    print('----------------------------------------'.ljust(40), end="")
    for header in table_headers:
        print('----------------------------------------'.ljust(40), end="")
    print()
    print("    usernames".ljust(40), end="")
    for header in table_headers:
        print(header.ljust(40), end="")
    print()
    print('----------------------------------------'.ljust(40), end="")
    for header in table_headers:
        print('----------------------------------------'.ljust(40), end="")

    unsecure_users = {}
    secure_user = {}
    expired_users = {}

    # sort the users into categories.
    for user in usernames:
        # if a user has a secure IP assigned, they are a secure user.
        if('Authorization_Server_IP_Secure' in data[user]):
            secure_user[user] = data[user]
        # if a user does not have a secure IP assigned but has logged in
        # securely in the past then they are an expired secure user.
        elif('Last_Secure_Login' in data[user]):
            expired_users[user] = data[user]
        # otherwise they are a general user.
        else:
            unsecure_users[user] = data[user]


    # pretty print the table rows.
    print("\nUnsecure Users")
    for username in unsecure_users:
        print_row(username, unsecure_users[username], table_headers, known_headers, "N/A")

    print("\nExpired Secure Users")
    for username in expired_users:
        print_row(username, expired_users[username], table_headers, known_headers, "Expired")

    print("\nSecure Users")
    for username in secure_user:
        print_row(username, secure_user[username], table_headers, known_headers, "Not Set")


# This function prints a row of the custom report based on the information
# extracted by the reporting system.
def print_row(username, user, table_headers, known_headers, not_set_message):
    print(("    " + username).ljust(40), end="")
    for column in table_headers:
        if (column in user):
            # Format the login information as a date.
            if (column == 'Last_Secure_Login'):
                login_time = time.localtime(int(user[column]['value']) / 1000)
                print(time.strftime('%Y-%m-%d %H:%M:%S', login_time).ljust(40), end="")
            else:
                print(user[column]['value'].ljust(40), end="")
        # If this known column does not exist for this user, print the 'not set' message.
        elif (column in known_headers):
            print(not_set_message.ljust(40), end="")
        # Leave unassigned custom columns (if any exist) blank.
        else:
            print("".ljust(40), end="")
    print()

if __name__ == "__main__":
    main()
