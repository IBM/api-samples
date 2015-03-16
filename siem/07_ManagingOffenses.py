#!/usr/bin/env python3
# This sample demonstrates how to use the siem endpoint in the
# REST API.

# Here we will be showing an example of how to manage offenses and users.
# The example shows how to assign offenses to people given the IP addresses
# of the destination_networks, and a way to keep up to date on which offenses
# need to be closed soon, and which offenses should have been closed by now.

# This sample uses a file (default assignment_data.csv)containing the data
# in the format:
# name,destination_network,days_to_close
# with commas separating the elements.
# For this sample to work all names must be existing users on the system.

# For this scenario to work there must already be offenses on the system the
# sample is being run against.
# THIS SAMPLE WILL MAKE CHANGES TO THE OFFENSES IT IS RUN AGAINST
# The scenario demonstrates the following actions:
#  - Using siem/offenses GET with filters and fields parameters
#  - Using data returned by API calls
#  - Assigning offenses using rules assigned in a separate file
#  - Managing offenses by assigning them to separate users and
#    using their creation date to enforce a timetable for dealing
#    with them.

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import json
import os
import sys
import urllib.parse
import datetime
sys.path.append(os.path.realpath('../modules'))

from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities


def main():
    # First we have to create our client
    client = RestApiClient(version='3.0')

    # In this half of the sample, we will show one way to use a csv file and
    # turn it into a dictionary. Then using that dictionary, and information on
    # the offenses, assign each unclosed offense to the correct person.

    # Read your raw string
    file_name = 'assignment_data.csv'
    file_in = open(file_name, 'r')

    # Break it into a list of lines
    file_data = file_in.read().splitlines()

    # This is the array of dictionaries we're going to be using to store the
    # data
    assignment_data = []
    # Iterate through each line, and taking each word separately organize them
    # in a dictionary for later use and put the dictionary into a list of
    # similar dictionaries.
    for data in file_data:
        data = data.split(',')
        tmp_dict = {}

        # Assign the offense to 'name'
        tmp_dict['name'] = data[0]

        # Given the 'destination_network'
        tmp_dict['destination_network'] = data[1]

        # And it should be resolved by 'days_to_resolve' days later
        tmp_dict['days_to_resolve'] = data[2]

        assignment_data.append(tmp_dict)

    # Display the new list of dictionaries
    print(json.dumps(assignment_data, indent=4))

    # Now that we have our rules set out for how to deal with offenses, we need
    # to GET the offenses. The only offenses we need to assign to people are
    # those that aren't CLOSED and aren't already assigned to someone.
    search = urllib.parse.quote('siem/offenses?filter=status!=CLOSED'
                                '&fields=id,description,'
                                'magnitude,destination_networks,assigned_to')

    # Call the API to GET the offenses
    SampleUtilities.pretty_print_request(client, search, 'GET')
    response = client.call_api(search, 'GET')

    # Ensure the call didn't fail for some reason.
    if (response.code != 200):
        print(
            'An error occured trying to get a list of offenses on the system.')
        SampleUtilities.pretty_print_response(response)
        exit(1)

    # Decode the offenses we just received from the API call and print them
    # out for the user to see.
    offense_list = json.loads(response.read().decode('utf-8'))
    print(json.dumps(offense_list, indent=4))

    # Check if the user really wants to proceed, as changes will be made to the
    # offenses
    while True:
        confirmation = input(
            'This sample is about to assign offenses to users as specified'
            ' by assignment_data.csv. Are you sure you want to proceed?'
            ' (YES/no) ')
        if (confirmation == 'YES'):
            break
        elif (confirmation == 'no'):
            print('You have chosen not to proceed with assigning offenses.')
            exit(0)
        else:
            print(confirmation + ' is not a valid answer.')

    # If there aren't any offenses, don't assign anything.
    if (len(offense_list) == 0):
        print('No offenses to assign')

    # If there ARE offenses...
    else:
        # Create a list of just the destination networks for quick access. It's
        # important that the new list is in the same order as the original
        assignment_networks = list(map(lambda assignment:
                                       assignment['destination_network'],
                                       assignment_data))

        # Now go through all the offenses
        for offense in offense_list:
            # A flag variable to show if the current offense has been assigned
            # to anybody yet.
            assigned = False

            # Now we take a look at all the destination_networks
            for target_ip in offense['destination_networks']:

                if target_ip in assignment_networks:
                    # Once we match a destination_network to one of the
                    # networks specified by our assignment rules, we need to
                    # find which rule, or line in the csv file, made a match
                    # with this current offense's destination_network
                    index = assignment_networks.index(target_ip)

                    # Once we know which rule matched with the
                    # destination_network, we can send in a POST call to update
                    # the offense's assigned_to variable, and by doing that
                    # assign the offense to the correct user.
                    update_request = urllib.parse.quote(
                        'siem/offenses/' + str(offense['id']) +
                        '?assigned_to=' + assignment_data[index]['name'])
                    response = client.call_api(update_request, 'POST')

                    # Check the response code
                    if (response.code == 200):
                        print('Offense ' + str(offense['id']) +
                              ' (destination network: ' + target_ip +
                              ') has been assigned to ' +
                              assignment_data[index]['name'] + '.')
                        # If the offense was assigned properly, flip the flag
                        assigned = True
                    else:
                        print('There was an error when assigning offense ' +
                              str(offense['id']))
                        SampleUtilities.pretty_print_response(response)
                    break
            # If the offense didn't make any matches in the
            # assignment_networks, or there was a problem calling the API,
            # display a special message.
            if (not assigned):
                print('Offense ' + str(offense['id']) + ' could not '
                      'be assigned because there is no valid user associated '
                      'with destination networks ' +
                      str(offense['destination_networks']) + '.')

    # Now that offenses have been assigned, we want to go through all of the
    # offenses that aren't closed and ARE assigned to people. Since we want
    # offenses to be closed within a certain time, we're going to be checking
    # that.

    # Send in the GET request
    search = urllib.parse.quote(
        'siem/offenses?filter=status!=CLOSED and assigned_to is not null&'
        'fields=id,description,start_time,destination_networks,assigned_to')
    SampleUtilities.pretty_print_request(client, search, 'GET')
    response = client.call_api(search, 'GET')

    # Check the response code for errors
    if (response.code != 200):
        print(
            'An error occured trying to get a list of offenses on the system.')
        SampleUtilities.pretty_print_response(response)
        exit(1)
    # Decode the response
    offense_list = json.loads(response.read().decode('utf-8'))

    # This loop is structurally similar to the one above

    if (len(offense_list) == 0):
        print('No offenses assigned')

    else:
        # Create two new maps of assignment_data, one with the
        # destination_networks and one with the names for quick access, since
        # both of these are necessary
        assignment_networks = list(map(lambda assignment:
                                       assignment['destination_network'],
                                   assignment_data))
        assignment_names = list(
            map(lambda name: name['name'], assignment_data))

        for offense in offense_list:
            # A flag variable to check if the offense has already existed
            # longer than the days_to_resolve
            late = False

            # A flag variable to check if the offense was assigned to a user in
            # assignment_data.csv
            match = False

            for target_ip in offense['destination_networks']:

                # Check the target_ip and the name of the user the offense was
                # assigned to.
                if ((target_ip in assignment_networks) and
                        (offense['assigned_to'] ==
                         assignment_names[
                            assignment_networks.index(target_ip)])):

                    # Trigger the flag to say this offense has been matched to
                    # a user-network pair in the assignment data
                    match = True

                    index = assignment_networks.index(target_ip)

                    # Get the current datetime and calculate the datetime for
                    # when the offense was created. We use these datetimes to
                    # calculate how long it's been since the offense was
                    # created. Divide start_time by 1000 since start_time is in
                    # milliseconds.
                    current_date = datetime.datetime.utcnow()
                    assignment_date = datetime.datetime.utcfromtimestamp(
                        offense['start_time']/1000)

                    elapsed_time = (current_date - assignment_date).days

                    # If the offense has existed longer than days_to_resolve,
                    # display an urgent message. Instead of displaying an
                    # urgent message, any number of things could be done. For
                    # example, if you include an email in the data file, then
                    # in this situation you could email the user responsible
                    # for the offense directly.
                    if elapsed_time > int(
                            assignment_data[index]['days_to_resolve']):
                        print('Notify ' + assignment_names[index] + ', ' +
                              ' offense ' + str(offense['id']) +
                              ' must be closed immediately.')
                        # Trigger the flag to say this offense is late
                        late = True
                        break
            # If it wasn't already late, and it was matched with an destination
            # network and user in assignment_data.csv display a message just to
            # indicate how long the offense has before it's late.
            if (not late and match):
                print('Please close offense ' + str(offense['id']) +
                      ' within ' + str(int(assignment_data[index]
                                           ['days_to_resolve']) - elapsed_time)
                      + ' days!')

if __name__ == "__main__":
    main()
