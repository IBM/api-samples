# QRadar API Samples

This package contains sample python code that demonstrates how to use the
QRadar REST API. The API is accessed by sending specially crafted HTTP
requests to specific URLs on the QRadar console. These URLs, known as
**“endpoints”**, each perform a specific function. Some endpoints perform
different functions depending on whether you send a GET, POST, or
DELETE request. By linking together calls to these endpoints you can
implement you own custom business processes or integrate QRadar data
with external systems.

This package is applicable to version 3.0 of the reference data and ariel APIs
and 1.0 of the help endpoint. A version number of 3.0 is used by default by
these samples since the API automatically selects the highest version less than
or equal to the requested version.
Endpoints released as **"Experimental"** may change in future versions of the API. In
general, past versions of the API remain available so these samples will
continue to run against version 3.0. When changes are made in future versions
of the API new samples will be released.

The QRadar REST API contains endpoints not covered by these samples.
Future releases of this sample package will be expanded to include
examples of more API endpoints.

For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page on your QRadar
installation at `https://<hostname>/api_doc`
You can retrieve a list of available endpoints from the API itself at
the `/help/capabilities` endpoint.

You can also join the community on our forums at:
https://www.ibm.com/developerworks/community/forums/html/forum?id=b02461a3-9a70-4d73-94e8-c096abe263ca


## What's new




## Package contents

 - An introduction package that shows how to use the API at a low level
 - A reference data package that demonstrates endpoints in the
    `/reference_data category`.
 - An Ariel package that demonstrates endpoints in the `/ariel` category.
 - An Offense package that demonstrates endpoints in the `/siem/offenses` category.
 - An API CLI client that can be used to access the API from the
    command line.
 - A package containing shared modules.


## Requirements

- Python 3.3 or above
- QRadar system 7.2.4 or higher


## Instructions

For the sample code to work without modifications, it is necessary that
the folder structure does not change.

To run a sample script from the command line navigate to the directory the
script is in and run `python <script_name.py>` replacing python with the 
name of your python 3 binary if it is different on your system. You can also
run these samples from your chosen python development environment as you
would run any other python script. You may need to run one sample from the
command line or set up you IDE's console to be interactive so that the
configuration file can be created.

If this is your first time running any of the samples, you will be prompted for
the IP address of your QRadar install. Authorize your session by supplying
an authorization token or by supplying a username and password.
Authorization tokens can be generated in **Authorized Services** under the
admin tab of the QRadar console.

Currently, it is strongly recommend that only administrators be granted access
to the QRadar Security Intelligence API.

Note that credentials are stored in plain text in a file called `config.ini`. IBM
recommends that you do not leave this file stored in your file system. You
should make sure to delete it when you are done with it.
By default this configuration file is stored at the root level of the samples
directory. From there all sample scripts, as well as the command line client,
will be able to use it.

Each sample directory also contains a `Cleanup.py` script that you can use
to remove the data created by the script from your system. Some scripts
include a line that you can uncomment to clean up the script's data as soon
as it is run. Data created by scripts is left on the system by default so that
you can see how it affects the system and so that you can experiment with it
either through the API or through the main UI. IBM recommends that you clean up
this sample data when you are done with it so that it does not get lost on your
system.


## Makeup of the config.ini file

```
[DEFAULT]
server_ip = {IP ADDRESS}
auth_token = {AUTH TOKEN} (Optional)
username = {USERNAME} (Optional)
password = {PASSWORD} (Optional)
```

If you are using the shared module `RestApiClient.py` to experiment with
writing your own API scripts there are several options available to you
for loading configurations other than the default configuration.
You can pass a different file name to have the Client load the configuration
from that file instead of the default. You can create a new configuration
section in the `config.ini` file and pass the name of that section.  
For example you could add a section

```
[my_custom_config]
username = {my_other_username}
password = {my_other_password}
```

to the configuration file and load your setting from there. Any required setting
not included in this custom section will be loaded from the default section.
You can also create you own dictionary of setting from some other source
and pass it directly to the RestApiClient.
