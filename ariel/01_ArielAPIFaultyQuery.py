#!/usr/bin/env python3
# This workflow will show how to handle errors returned by the API.
# If a faulty expression is sent to the ArielAPI, a response object with an
# error will be returned. The error gets read out.


def main():
    import sys
    import os
    sys.path.append(os.path.realpath('../modules'))
    import json
    from arielapiclient import APIClient

    # Creates an instance of APIClient, which contains all the API methods.
    api_client = APIClient()

    # The AQL expression that will be sent for the search.
    # It is faulty.
    query_expression = "SELECT foobar from events"
    # If no search_id is provided, one will be generated.

    # A method is called by using the query parameters above. This will
    # call POST /searches on the Ariel API. (See the ArielAPIClient for more
    # detail).
    # This method returns a response object created by urllib.request library.
    response = api_client.create_search(query_expression, '2')

    # Each response contains an HTTP response code.
    #  - Response codes in the 200 range indicate that your request succeeded.
    #  - Response codes in the 400 range indicate that your request failed due
    #    to incorrect input.
    #  - Response codes in the 500 range indicate that there was an error on
    #    the server side.
    print(response.code)

    # A response object is returned. It informs if the request is
    # successful or not successful. A searchID that is
    # necessary when retrieving the results of the search is returned.

    # The search is asynchronous. The response will not be the result of
    # the search.

    # The two lines below parse the body of the response (a JSON object)
    # into a dictionary so that you can discern information, such as the
    # searchID.
    response_json = json.loads(response.read().decode('utf-8'))
    print(json.dumps(response_json, indent=2, separators=(',', ':')))

if __name__ == "__main__":
    main()
