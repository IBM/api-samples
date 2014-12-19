#!/usr/bin/env python3
# This sample demonstrates how to use the siem endpoint in the
# REST API.

# For this scenario to work there must already be offenses on the system the
# sample is being run against.  The scenario demonstrates the following actions:
#  - How to get offenses.
#  - How to filter the data that is returned with the fields parameter.
#  - How to filter the data that is returned with the filter parameter.
#  - How to page through the results using the range parameter.

# To view a list of the endpoints with the parameters they accept, you can view
# the REST API interactive help page on your deployment at
# https://<hostname>/api_doc.  You can also retrieve a list of available
# endpoints with the REST API itself at the /api/help/capabilities endpoint.

import json
import os
import sys
sys.path.append(os.path.realpath('../modules'))

from RestApiClient import RestApiClient
import SampleUtilities as SampleUtilities

def main():
	# First we have to create our client
	client = RestApiClient()


	#----------------------------------------------------------------------------#
	#Basic 'GET'
	# In this example we'll be using the GET endpoint of siem/offenses without
	# any parameters. This will print absolutely everything it can find, every
	# parameter of every offense.

	# Send in the request
	SampleUtilities.pretty_print_request(client, 'siem/offenses', 'GET')
	response = client.call_api('siem/offenses', 'GET')

	# Check if the success code was returned to ensure the call to the API was
	# successful.
	if (response.code != 200):
		print('Failed to retrieve the list of offenses')
		SampleUtilities.pretty_print_response(response)
		sys.exit(1)

    # Since the previous call had no parameters and response has a lot of text,
	# we'll just print out the number of offenses 
	response_body = json.loads(response.read().decode('utf-8'))
	print('Number of offenses retrived: ' + str(len(response_body)))
	

	#----------------------------------------------------------------------------#
	#Using the fields parameter with 'GET'	
	# If you just print out the result of a call to the siem/offenses GET endpoint
	# there will be a lot of fields displayed which you have no interest in.
	# Here, the fields parameter will make sure the only the fields you want
	# are displayed for each offense.

	# Setting a variable for all the fields that are to be displayed
	fields = '''id,status,description,offense_type,offense_source,magnitude,\
source_network,destination_networks,assigned_to'''

	# Send in the request
	SampleUtilities.pretty_print_request(client, 'siem/offenses?fields=' + fields, 'GET')
	response = client.call_api('siem/offenses?fields=' + fields, 'GET')

	# Once again, check the response code
	if (response.code != 200):
		print('Failed to retrieve list of offenses')
		SampleUtilities.pretty_print_response(response)
		sys.exit(1)

	# This time we will print out the data itself
	SampleUtilities.pretty_print_response(response)


	#----------------------------------------------------------------------------#
	#Using the filter parameter with 'GET'
	# Sometimes you'll want to narrow down your search to just a few offenses.
	# You can use the filter parameter to carefully select what is returned
	# after the call by the value of the fields.
	# Here we're only looking for OPEN offenses, as shown by the value of 'status'
	# being 'OPEN' 
	
	# Send in the request
	SampleUtilities.pretty_print_request(client, 'siem/offenses?fields=' + fields + 
			'&filter=status=OPEN', 'GET')
	response = client.call_api('siem/offenses?fields=' + fields + '&filter=status=OPEN', 'GET')

	# Always check the response code
	if (response.code != 200):
		print('Failed to retrieve list of offenses')
		SampleUtilities.pretty_print_response(response)
		sys.exit(1)

	# And output the data
	SampleUtilities.pretty_print_response(response)


	#----------------------------------------------------------------------------#
	#Paging the 'GET' data using 'Range'
	# If you have a lot of offenses, then you may want to browse through them
	# just a few at a time. In that case, you can use the Range header to 
	# limit the number of offenses shown in a single call. 

	# In this example only OPEN offenses will be used.

	# Call the endpoint so that we can find how many OPEN offenses there are.
	response = client.call_api('siem/offenses?filter=status=OPEN', 'GET')
	num_of_open_offenses = len(json.loads(response.read().decode('utf-8')))

	# Copy the headers into our own variable
	range_header = client.get_headers().copy()

	# Set the starting point (indexing starts at 0)
	page_position = 0
	# and choose how many offenses you want to display at a time.
	offenses_per_page = 5

	# Looping here in order to repeatedly show 5 offenses at a time until we've
	# seen all of the OPEN offenses or exit character q is pressed
	input_string = ""
	while True:

		# Change the value for Range in the header in the format item=x-y
		range_header['Range'] = 'items=' + str(page_position) + '-' + str(page_position + offenses_per_page - 1)

		# Send in the request
		SampleUtilities.pretty_print_request(client,'siem/offenses?fields=' + fields + 
			'&filter=status=OPEN', 'GET', headers=range_header)
		response = client.call_api('siem/offenses?fields=' + fields + 
			'&filter=status=OPEN', 'GET', headers=range_header)

		# As usual, check the response code
		if (response.code != 200):
			print('Failed to retrieve list of offenses')
			SampleUtilities.pretty_print_response(response)
			sys.exit(1)

		# Output the data
		SampleUtilities.pretty_print_response(response)
	
		# Check to see if all the offenses have been displayed
		if (page_position + offenses_per_page >= num_of_open_offenses):
			print('All offenses have been printed to the screen.')
			break
		else:
			# Wait for the user to display the next set or quit
			input_string = input('Push enter to bring up the next ' +
								 str(offenses_per_page) + ' offenses, or q to quit. ')
			# If the user entered the character 'q', quit.
			if (input_string == 'q'):
				break
			page_position += offenses_per_page

if __name__ == "__main__":
    main()
