# QRadar API Samples

This package contains sample Python code that demonstrates how to use the
QRadar REST API. The API is accessed by sending specially crafted HTTP
requests to specific URLs on the QRadar console. These URLs, known as
**"endpoints"**, each perform a specific function. Some endpoints perform
different functions depending on whether you send a GET, POST, or
DELETE request. By linking together calls to these endpoints you can
implement you own custom business processes or integrate QRadar data
with external systems.

The QRadar REST API contains endpoints not covered by these samples.
Future releases of this sample package will be expanded to include
examples of more API endpoints.

For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page on your QRadar
installation at `https://<hostname>/api_doc`
You can retrieve a list of available endpoints from the API itself at
the `/help/endpoints` endpoint.

You can also join the community on our forums at:
https://www.ibm.com/developerworks/community/forums/html/forum?id=b02461a3-9a70-4d73-94e8-c096abe263ca


## What's New
For the changes to the API's and the impacts those would have on the samples see
[What's new for developers in RESTful APIs in QRadar V7.2.8](http://www.ibm.com/support/knowledgecenter/en/SS42VS_7.2.8/com.ibm.qradar.doc/c_rest_api_whatsnew_detail.html).


## Package Contents

 - An introduction package that shows how to use the API at a low level.
 - A reference data package that demonstrates endpoints in the
    `/reference_data` category.
 - An Ariel package that demonstrates endpoints in the `/ariel` category.
 - An Offense package that demonstrates endpoints in the `/siem/offenses` category.
 - A Domain Management package that demonstrates endpoints in the
   `/config/domain_management/domains` category.
 - A Custom Actions package that demonstrates endpoints in the 
   '/analytics/custom_actions' category.
 - An API CLI client that can be used to access the API from the
    command line.
 - A package containing shared modules.


## Requirements

- Python 3.3 or above
- QRadar system 7.2.8 or higher


## Instructions

The API samples should not be run directly on a QRadar appliance. The API
samples are intended to run on an outside system to poll data from QRadar.
QRadar does not run Python 3.3 and the requirements for Python 3.3 is intended
for the outside host that is running the code samples. QRadar cannot be
upgraded to Python 3.3 as this will cause system-wide issues. Adminsitrators
should never be installing any RPMs on their QRadar Console, unless the files
come from IBM Fix Central.

For the sample code to work without modifications, it is necessary that
the folder structure does not change.

To run a sample script from the command line navigate to the directory the
script is in and run `python <script_name.py>` replacing python with the 
name of your Python 3 binary if it is different on your system. You can also
run these samples from your chosen Python development environment as you
would run any other Python script. You may need to run one sample from the
command line or set up you IDE's console to be interactive so that the
configuration file can be created.

If this is your first time running any of the samples, you will be prompted for
the configuration details. Configuration details include:

 - IP address or domain name of your QRadar install.
 - Credentials.  Either username and password or an authorized service token.
 - Optional TLS certificate.

Authorization tokens can be generated in **Authorized Services** under the
admin tab of the QRadar console.

The TLS certificate is optional, but must be provided if your system uses a
self signed TLS certificate. See the [TLS Certificate][] section for more
information.

After entering configuration details for the sample you will be prompted asking
if you would like to save the configuration to disk. If you choose to store the
configuration it will be stored in plain text unencrypted in a file called
`config.ini`. IBM recommends that you do not store sensitive credentials in
this file. If you choose not to save the configuration details in the file you
will be prompted to enter the configuration details each time you run a sample.
This configuration file is stored at the root level of the samples directory.
From there all sample scripts, as well as the command line client, will be able
to use it.

Some sample directories also contains a `Cleanup.py` script that you can use
to remove the data created by the samples from your system. Some scripts
include a line that you can uncomment to clean up the script's data as soon
as it is run. Data created by scripts is left on the system by default so that
you can see how it affects the system and so that you can experiment with it
either through the API or through the main UI. IBM recommends that you clean up
this sample data when you are done with it.

## TLS Certificate

When entering the configuration details you have the option of providing a TLS
certificate file. This is required when your QRadar system uses a self signed
certificate. When prompted enter the path to the certificate stored in PEM
format.

Use one of the following methods to obtain the certificate file:

 - Copy the certificate file from the QRadar box. The QRadar certificate is
   stored at `/etc/httpd/conf/certs/cert.cert`.
 - Export the certificate in PEM format from your browser.

When you manually obtain and specify the certificate file it is your
responsibility to verify the certificate authenticity.

If you are using a CA with untrusted root or intermediate certificates,
the file specified by certificate_file must contain the full chain. For
more information, see the [Python documentation](https://docs.python.org/3/library/ssl.html#ssl.SSLContext.load_verify_locations).

## Makeup of the config.ini file

```
[DEFAULT]
server_ip = {IP ADDRESS}
auth_token = {AUTH TOKEN} (Optional)
username = {USERNAME} (Optional)
password = {PASSWORD} (Optional)
certificate_file = {CERTIFICATE FILE} (Optional)
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

These samples are provided for reference purposes on an "as is" basis, and are
without warranties of any kind.

It is strongly advised that these samples are not run against production
systems.

Any issues discovered using the samples should not be directed to QRadar
support, but be reported on the Github issues tracker.
