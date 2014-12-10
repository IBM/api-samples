from RestApiClient import RestApiClient
import urllib.parse


# Inherits methods from APIClientBase
class APIClient(RestApiClient):

    # API METHODS

    # These methods are used to call Ariel's API methods through http requests.
    # Each method makes use of the http methods below to perform the requests.

    # This class will encode any data or query parameters which will then be sent
    # to the call_api() method of its inherited class.
    def __init__(self, settings=None):


        self.endpoint_start = 'ariel/'
        super(APIClient, self).__init__(settings=settings)

    def get_databases(self):

        endpoint = self.endpoint_start + 'databases'
        # Sends a GET request to
        # https://<server_ip>/rest/api/ariel/databases
        return self.call_api(endpoint, 'GET', self.headers)

    def get_database(self, database_name):

        endpoint = self.endpoint_start + 'databases' + '/' + database_name
        # Sends a GET request to
        # https://<server_ip>/rest/api/ariel/databases/<database_name>
        return self.call_api(endpoint, 'GET', self.headers)

    def get_searches(self):

        endpoint = self.endpoint_start + "searches"
        # sends a GET request to https://<server_ip>/rest/api/ariel/searches
        return self.call_api(endpoint, 'GET', self.headers)

    def create_search(self, query_expression, query_language_version=None, search_id=None, start_time=None, end_time=None):

        endpoint = self.endpoint_start + "searches"
        # sends a POST request to https://<server_ip>/rest/api/ariel/searches

        data = {'query_expression': query_expression}
        if query_language_version:
            data['query_language_version'] = query_language_version
        if search_id:
            data['search_id'] = search_id
        if start_time:
            data['start_time'] = start_time
        if end_time:
            data['end_time'] = end_time

        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')

        return self.call_api(endpoint, 'POST', self.headers, data=data)

    def get_search(self, search_id):

        # Sends a GET request to
        # https://<server_ip>/rest/api/ariel/searches/<search_id>
        endpoint = self.endpoint_start + "searches/" + search_id

        return self.call_api(endpoint, 'GET', self.headers)

    def get_search_results(self, search_id,
                           response_type, range_start=None, range_end=None):

        headers = self.headers.copy()
        headers[b'Accept'] = response_type
        
        if ( (range_start is not None) and (range_end is not None) ):
            headers[b'Range'] = 'items=' + str(range_start) + '-' + str(range_end)

        # sends a GET request to
        # https://<server_ip>/rest/api/ariel/searches/<search_id>
        endpoint = self.endpoint_start + "searches/" + search_id + '/results'

        # response object body should contain information pertaining to search.
        return self.call_api(endpoint, 'GET', headers)

    def update_search(self, search_id, save_results=None, status=None):

        # sends a POST request to
        # https://<server_ip>/rest/api/ariel/searches/<search_id>
        # posts search result to site
        endpoint = self.endpoint_start + "searches/" + search_id

        data = {}
        if save_results:
            data['save_results'] = save_results
        if status:
            data['status'] = status

        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')

        return self.call_api(endpoint, 'POST', self.headers, data=data)

    def delete_search(self, search_id):

        # sends a DELETE request to
        # https://<server_ip>/rest/api/ariel/searches/<search_id>
        # deletes search created earlier.
        endpoint = self.endpoint_start + "searches" + '/' + search_id

        return self.call_api(endpoint, 'DELETE', self.headers)
