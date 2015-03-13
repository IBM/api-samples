from RestApiClient import RestApiClient
import urllib.parse

# Inherits methods from RestApiClient
class APIClient(RestApiClient):

    #API METHODS

    # The following methods will call the Ariel API methods through http
    # requests. Each method makes use of the The following http methods to
    # perform the requests.

    # This class will encode any data or query parameters and will be sent
    # to the call_api() method of its inherited class.
    def __init__(self, config_section='DEFAULT', config=None):


        self.endpoint_start = 'ariel/'
        super(APIClient, self).__init__(config_section=config_section,
                                        version='1.0', config=config)

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
        # Sends a GET request to https://<server_ip>/rest/api/ariel/searches
        return self.call_api(endpoint, 'GET', self.headers)

    def create_search(self, query_expression, query_language_version=None, search_id=None, start_time=None, end_time=None):

        endpoint = self.endpoint_start + "searches"
        # A POST request is sent to https://<server_ip>/rest/api/ariel/searches.

        data = {'queryExpression': query_expression}
        if query_language_version:
            data['queryLanguageVersion'] = query_language_version
        if search_id:
            data['searchID'] = search_id
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time

        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')

        return self.call_api(endpoint, 'POST', self.headers, data=data)

    def get_search(self, search_id):

        # A GET request is sent to
        # https://<server_ip>/rest/api/ariel/searches/<search_id>.

        endpoint = self.endpoint_start + "searches/" + search_id
        
        return self.call_api(endpoint, 'GET', self.headers)

    def get_search_results(self, search_id,
                           response_type, range_start=None, range_end=None):

        headers = self.headers.copy()
        headers[b'Accept'] = response_type

        # A GET request is sent to
        # https://<server_ip>/rest/api/ariel/searches/<search_id>.

        endpoint = self.endpoint_start + "searches/" + search_id + '/results'

        params = [['rangeStart', range_start],['rangeEnd', range_end]]
       
        # Information pertaining to search is stored in response object body.
        return self.call_api(endpoint, 'GET', headers, params=params)

    def update_search(self, search_id, save_results=None, status=None):

        # A POST request is sent to, and the search result is posted
        # to https://<server_ip>/rest/api/ariel/searches/<search_id>.
         
        endpoint = self.endpoint_start + "searches/" + search_id
        
        data = {}
        if save_results:
            data['saveResults'] = save_results
        if status:
            data['status'] = status

        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')

        return self.call_api(endpoint, 'POST', self.headers, data=data)

    def delete_search(self, search_id):

        # A DELETE request is sent to
        # https://<server_ip>/rest/api/ariel/searches/<search_id>.
        # The previous search is deleted.
        endpoint = self.endpoint_start + "searches" + '/' + search_id
        
        return self.call_api(endpoint, 'DELETE', self.headers)
