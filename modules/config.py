import configparser
import os
import sys
import RestApiClient
import getpass
import json


class Config:
    """
    Prompt the user for configuration settings. The user has the option to save
    the settings into a configuration file, but this is not required.
    """

    def __init__(self, config_file='config.ini', config_section='DEFAULT'):
        """
        Generate a new Config object. If config_file already exists and
        server_ip is defined in the INI configuration section config_section
        then the settings are read from the config_file. Otherwise the user is
        prompted for the settings and given the option to save the settings to
        config_file. config_file is read from and written to the root of the
        samples directory.
        """

        # Read config_file from the root of the samples directory.
        config_file = os.path.abspath(os.path.dirname(__file__) +
                                      '/../' + config_file)

        self.config_file = config_file
        self.config_section = config_section

        self.config = configparser.ConfigParser()

        create_new_config = True
        if os.path.isfile(config_file):

            self.config.read(config_file)
            if 'server_ip' in self.config[config_section]:
                create_new_config = False

        if create_new_config:

            self._create_new_config()

    def has_config_value(self, config_name):
        """
        Return true if a value for config_name exists in the configuration.
        """

        return config_name in self.config[self.config_section]

    def get_config_value(self, config_name):
        """
        Return the value for config_name, or None if no value for config_name
        exists in the configuration.
        """

        if config_name in self.config[self.config_section]:
            return self.config[self.config_section][config_name]
        else:
            return None

    def set_config_value(self, config_name, config_value):
        """
        Set the value of config_name to config_value.
        """

        self.config[self.config_section][config_name] = config_value

    def write_config_file(self):
        """
        Prompt the user asking if they would like to save the settings,
        including credentials, unencrypted. If they respond yes then save the
        settings to the config file. The Config instance will still work even
        if the settings are not saved to a file.
        """

        choice = _choice("ATTENTION:  It is recommended that you do not " +
                         "leave secure credentials saved unencrypted.\n" +
                         "Store authorization token or password " +
                         "unencrypted: (yes/no)? ",
                         valid_values=("yes", "no"))
        if choice == "yes":
            with open(self.config_file, 'w') as config_file_handle:
                self.config.write(config_file_handle)

    def _create_new_config(self):
        """
        Prompt the user for configuration values. Test if the configuration is
        valid by calling the /help/versions endpoint. If the configuration is
        valid call write_config_value(). If the configuration is not valid
        sys.exit(2) is called.
        """

        config_dict = {}

        config_dict['server_ip'] = input("Please input the IP address or " +
                                         "the hostname of the server you " +
                                         "want to connect to: ").strip()

        choice = _choice("Choose one of the following options for " +
                         "authentication: \n" +
                         "\t1. Authorization token (recommended).\n" +
                         "\t2. Username and password.\n" +
                         "Choice: ", valid_values=("1", "2"))

        if choice == "1":
            config_dict['auth_token'] = input(
                "Please input authorization token: ").strip()
        else:
            config_dict['username'] = input("Username: ").strip()
            config_dict['password'] = getpass.getpass("Password: ")

        certificate_file = _choice("Enter path to TLS PEM certificate " +
                                   "(optional): ", optional=True,
                                   file_exists=True)
        if certificate_file is not None:
            config_dict['certificate_file'] = certificate_file

        self.config[self.config_section] = config_dict

        self._verify_config()

        self.write_config_file()

    def _verify_config(self):
        """
        Verify the configuration is valid by calling the /help/versions
        endpoint. If the request fails print a message indicating the cause of
        the failure and then call sys.exit(2).
        """

        fail_message = None
        try:
            api_client = RestApiClient.RestApiClient(config=self)

            # Only request the /help categories to limit the size of the
            # response.
            params = {'categories': "['/help']"}
            response = api_client.call_api('/help/versions', 'GET',
                                           params=params)
            response.read()
            if response.code == 401 or response.code == 403:
                fail_message = "Authorization failed."
            elif response.code < 200 or response.code > 299:
                response_json = json.loads(response.read().decode('utf-8'))
                fail_message = response_json['http_response']['message']
                fail_message += "\n" + response_json['message']
        except Exception as e:
            fail_message = str(e)

        if fail_message is not None:
            print("Configuration validation failed.")
            print(fail_message)
            print("Check your settings.")
            sys.exit(2)


def _choice(prompt, valid_values=None, file_exists=False, optional=False):
    """
    A method used to help prompt the user for input and validate user input. If
    valid_values is provided _choice confirms the input is in valid_values and
    returns the input. If file_exists is True _choice confirms the file exists
    and returns the absolute path of the file. If optional is True then None
    will be returned if the user does not provide any input.
    """

    choice = input(prompt).strip()
    if optional and choice == "":
        return None

    if valid_values is not None:
        while choice not in valid_values:
            print(choice + " is not a valid option.")
            choice = input(prompt).strip()
            if optional and choice == "":
                return None
    elif file_exists:
        while not os.path.isfile(choice):
            print("File " + choice + " does not exist.")
            choice = input(prompt).strip()
            if optional and choice == "":
                return None
        return os.path.abspath(choice)

    return choice
