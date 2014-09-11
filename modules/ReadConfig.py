try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import sys
import os
import base64


def display_config_file(configFile):
    print(configFile)
    return


def check_for_config_file(dir_name, file_name):
    filename = os.path.join(dir_name, file_name)
    if os.path.isfile(filename):
        return filename
    else:
        return None


################################################################
# We need a configuration file to run.
# The file can be passed in as a parameter, but the default is one level up
# from the current working directory so that the sample scripts can share
# the same configuration file
################################################################
def getConfigFile(file_name):

    # Check the specified directory for the config file
    cwd = os.getcwd()
    configFile = check_for_config_file(cwd, file_name)
    if configFile is not None:
        return configFile


# This function takes a username and password and encodes them in the manner
# required to properly authenticate to the API.
# the format is 'Basic base64_encode(username:password)'
def encode_credentials(username, password):
    userpass = username + ":" + password
    return b"Basic " + base64.b64encode(userpass.encode('ascii'))


# This function parses the contents of the config file and returns a formatted
# settings dictionary
def parse_settings(config, config_section):

    if sys.version_info >= (3, 0):
        settings = {'version': '2.0',
                            'accept': 'application/json',
                            'server_ip': config[config_section]['server_ip']}
        if 'root_password' in config[config_section]:
            settings['root_password'] = config[config_section]['root_password']
        if 'auth_token' in config[config_section]:
            settings['auth_token'] = config[config_section]['auth_token']
        else:
            authorization = encode_credentials(
                config[config_section]['username'],
                config[config_section]['password'])
            settings['authorization'] = authorization

    else:
        settings = {'version': '1.0',
                        'accept': 'application/json',
                        'server_ip': config.get(config_section, 'server_ip')}
        try:
            settings['root_password'] = config.get(config_section, 'root_password')
        except:
            pass
        try:
            settings['auth_token'] = config.get(config_section, 'auth_token')
        except:
            authorization = encode_credentials(
                config.get(config_section, 'username'),
                config.get(config_section, 'password'))
            settings['authorization'] = authorization

    return settings


# This function reads the config file for disk and passes it on to be parsed
def import_config(configFile, config_section):
    config = configparser.ConfigParser()
    config.read(configFile)

    try:
        return parse_settings(config, config_section)
    except KeyError as e:
        print("Please supply value for " + str(e) +
              " in config file.\n")
        sys.exit(2)
    except configparser.NoOptionError as e:
        print("Please supply correct values in config file.")
        print(str(e))
        sys.exit(2)


# The main entry point to ReadConfig
def main(config_section='DEFAULT', file_name="../config.ini"):
    configFile = getConfigFile(file_name)
    if configFile is not None:
        return import_config(configFile, config_section)

if __name__ == "__main__":
    main()
