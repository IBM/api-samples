import configparser
import getpass
import json
import re
import sys
from urllib.error import HTTPError
from urllib.request import Request
from urllib.request import urlopen

import ReadConfig


inputter = input



# Check to make sure the provided ip address is valid
def validate_ip(ip):
    patt = re.compile('''
            ^                                       # Match start of string
            ([2][0-5][0-5]|^[1]{0,1}[0-9]{1,2})     # Match decimal octet
            \.                                      # Match '.' character
            ([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})    # Match decimal octet
            \.                                      # Match '.' character
            ([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})    # Match decimal octet
            \.                                      # Match '.' character
            ([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})    # Match decimal octet
            $                                       # Match end of string
            ''', re.VERBOSE)
    m = re.search(patt, ip.split()[-1])

    if m:
        return True
    else:
        return False


# This function tests the configuration details entered to make sure they work.
def test_config(config):
    settings = ReadConfig.parse_settings(config, 'DEFAULT')

    # set up a request based on the settings we created
    # do it here so that we are not dependent on other API client files
    headers = {b'Version': settings['version'], b'Accept': settings['accept']}

    if 'auth_token' in settings:
        auth = {'SEC': settings['auth_token']}
    else:
        auth = {'Authorization': settings['authorization']}

    headers.update(auth)

    request = Request(
            'https://' + settings['server_ip'] + '/restapi/api/help/capabilities', headers=headers)
    try:
        # returns response object for opening url.
        return urlopen(request)
    except HTTPError as e:
        # an object which contains information similar to a request object
        return e


# The main entry point for MakeConfig
def main(file_name='../config.ini'):

    ip = inputter("Please input the IP address of the server you want to connect to: ")
    while not validate_ip(ip):
        print("Invalid IP")
        ip = inputter("Please input the IP address of the server you want to connect to: ")

    config_dict = {'server_ip': ip}

    choice = inputter("Choose one of the following options for authentication: "
                        + "\n1. Authorization token (recommended)."
                        + "\n2. Username and password.\nChoice: ")
    while choice != '1' and choice != '2':
        choice = inputter("\nInvalid choice!"
                            + "\nChoose one of the following options for authentication: "
                            + "\n1. Authorization token (recommended)."
                            + "\n2. Username and password.\nChoice: ")

    if choice == '1':
        auth_token = inputter("Please input authorization token: ")
        config_dict['auth_token'] = auth_token
    else:
        username = inputter("Username: ")
        password = getpass.getpass("Password: ")
        config_dict['username'] = username
        config_dict['password'] = password

    config = configparser.ConfigParser()
    if sys.version_info >= (3, 0):
        config['DEFAULT'] = {}
        for each in config_dict:
            config['DEFAULT'][each] = config_dict[each]
    else:
        for each in config_dict:
            config.set('DEFAULT', each, config_dict[each])

    print("Testing configuration ... ")
    response = test_config(config)
    if response.code == 200:
        print("Config valid, writing to file.")
        f = open(file_name, 'w')
        config.write(f)
    elif response.code == 401:
        print("Config invalid: Authentication failed.\n"
                + "Check your authorization credentials.")
        sys.exit(2)
    else:
        print("An unexpected error occurred setting up the config file:")
        print(response.code)
        parsed_response = json.loads(response.read().decode('utf-8'))
        print(json.dumps(parsed_response, indent=4))
        sys.exit(2)



if __name__ == "__main__":
    main()
