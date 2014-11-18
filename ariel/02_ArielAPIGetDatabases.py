# This workflow calls the Ariel API to return a list of all databases
# that can be queried by Ariel API methods.


def main():
    import sys
    import os
    sys.path.append(os.path.realpath('../modules'))
    from arielapiclient import APIClient
    import json

    # Creates an instance of APIClient, which contain all API methods.
    api_client = APIClient()

    # Calls GET /databases in the Ariel API
    # Response body contains a JSON object of searchable databases.
    response = api_client.get_databases()

    # Each response contains an HTTP response code.
    # Response codes in the 200 range indicate that your request succeeded.
    # Response codes in the 400 range indicate that your request failed due to incorrect input.
    # Response codes in the 500 range indicate that there was an error on the server side.
    print(response.code)

    # When a JSON object is requested, the Body of the object is decoded into a JSON object.

    response_json = (json.loads(response.read().decode('utf-8')))

    # Prints the contents of the JSON object.
    print(response_json)

if __name__ == "__main__":
    main()
