# Modified by Thijs Villevoije
#!/usr/bin/env python3
# This is an universal way to query to the ArielAPI, and receive
# the results. ArielAPI searches are asynchronous.
# Endpoints are used to determine if the search has completed.
# After determining that the search is complete, call
# GET /searches/{search_id}/results for search results.
# The results are saved through the POST /searches/{search_id} endpoint.


def main():
    import sys
    import os
    sys.path.append(os.path.realpath('../modules'))
    import json
    from arielapiclient import APIClient
    print("Please give the AQL search and press enter: ")
    
   
    # Creates instance of APIClient. It contains all of the API methods.
    api_client = APIClient()
    # While loop is created to make sure that whenever a wrong AQL is given,
    # the script doesn't terminate but asks for the AQL again, this to make it better usable.
    x=0
    while x==0:
        aqlsearch=input()
    # This is the AQL expression to send for the search.
        query_expression = str(aqlsearch)


    # Use the query parameters above to call a method. This will call
    # POST /searches on the Ariel API. (look at arielapiclient for more
    # detail).  A response object is returned. It contains
    # successful or not successful search information.
    # The search_id corresponding to this search is contained in
    # the JSON object.
        response = api_client.create_search(query_expression, '2')

    # Each response contains an HTTP response code.
    # Response codes in the 200 range indicate that your request succeeded.
    # Response codes in the 400 range indicate that your request failed due to incorrect input.
    # Response codes in the 500 range indicate that there was an error on the server side.
    # Only if the response code is in the 200 range results will be given
        temp=response.code
        temp=temp/100
    # If statement makes sure only when request succeed output will be printed
        if temp<=3:
            x=1
        else:
            print("This is not a proper AQL Search please try again: ")
        
    

    # The search is asynchronous, so the response will not be the results of
    # the search.

    # The 2 lines below parse the body of the response (a JSON object)
    # into a dictionary, so we can discern information, such as the search_id.
    response_json = json.loads(response.read().decode('utf-8'))

    # Prints the contents of the dictionary.
    #print(response_json)

    # Retrieves the search_id of the query from the dictionary.
    search_id = response_json['search_id']

    # This block of code calls GET /searches/{search_id} on the Ariel API
    # to determine if the search is complete. This block of code will repeat
    # until the status of the search is 'COMPLETE' or there is an error.
    response = api_client.get_search(search_id)
    error = False
    while (response_json['status'] != 'COMPLETED') and not error:
        if (response_json['status'] == 'EXECUTE') | \
                (response_json['status'] == 'SORTING') | \
                (response_json['status'] == 'WAIT'):
            response = api_client.get_search(search_id)
            response_json = json.loads(response.read().decode('utf-8'))
        else:
           # print(response_json['status'])
            error = True

    # After the search is complete, call the GET /searches/{search_id} to obtain
    # the result of the search.
    # Depending on whether the "application/json" or "application/csv"
    # method is given, return search results will be in JSON form or CSV form.
    response = api_client.get_search_results(
        search_id, 'application/json', '1', '11')

    body = response.read().decode('utf-8')
    body_json = json.loads(body)

    # This is for pretty printing the JSON object.
    #print(json.dumps(body_json, indent=2, separators=(',', ':')))

    # This is the same call as before, but asks for a CSV object in return.
    response = api_client.get_search_results(search_id, "application/csv")
    print("\n" + response.read().decode('utf-8'))

    # This method calls POST /searches/{search_id}. It saves the result of a
    # search to a disk.
    query_params = {"saveResults": "true"}
    response = api_client.update_search(search_id, query_params)


if __name__ == "__main__":
    main()
