# Reference Data Samples

Scripts in this directory demonstrate how to use the `/reference_data`
endpoints of the API.


For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`  
You can also retrieve a list of available endpoints through the api itself
at the `/api/help/capabilities` endpoint.


The scripts in this directory include:

### 01_Sets.py
In this sample you will see how data in reference sets can be
manipulated using the REST API.

In this scenario we have already configured two reference sets in the
product, one to capture ip addresses exhibiting suspect behavior and 
another to hold blocked ip addresses.

A custom rule is defined to identify suspect ip addresses based on
business rules.
A second rule is defined to generate offenses based on blocked ip
addresses accessing certain network resources.

Our company has a legacy system that contains data and software that
can choose ip addresses to block based on custom criteria and upload
these IP addresses to our company's firewalls. We would like to 
integrate this logic with the data in our reference set so that suspected ip
addresses collected by the product can be validated by this system and so
that ip addresses blocked by this system can be monitored by the product to
ensure they are properly excluded from our network.


### 02_Maps.py
In this example we will see how data in reference maps can be
manipulated using the REST API.

Our organization has several secure servers that can only be accessed
by security administrators. These administrators can only access these
servers during their scheduled shift and only one administrator is ever
on duty for a single server at one time (although one administrator can
supervise several servers at once). Furthermore some servers are not
used during some shifts and so should not be accessed at all during this
time.

Our human resources system tracks the shift schedule of our security
administrators and maintains a list of the servers that each one is
supervising. We would like to use this information to generate offenses
if any of these servers are improperly accessed.

We have already created a reference data map on our system that
matches the ip addresses of our servers to the user names of the 
administrators that can access them. We have also created a rule that 
generates an offense if any access is made to the servers by users not in
the reference map.


### 03_MapOfSets.py
In this example we will see how data in reference maps of sets can be
manipulated using the REST API.

Our company is an E-retailer serving customers around the world. We
have a number of authentication servers that allow our customers to log
in securely to our site. The CIO of our company believes that as our business
is growing these servers are becoming a bottleneck. He wants to monitor the
activity on these servers in real time through the digital dashboard of his
executive support system.

You have already created a rule on our system that captures login events on
the company's authentication servers and adds information about the login to
a reference data map of sets. The map uses the IP addresses of the servers
as keys, and stores the usernames that log in through those servers in the
sets.


### 04_Tables.py
In this example we will see how data in reference tables can be manipulated
using the REST API.
 
Our company has has a multi-level security authorization architecture. Users
are assigned an authorization server that they must use to log in to the
network. Once inside the general network, some users are authorized to access
the secure network. They use a different authorization server and must
connect through an assigned port.  
We have set up a reference table that stores the ip addresses of the server
that each user must use to login to the network. It also stores the ip
address and port of the secure server that authorized users must use to
connect to the secure network. We also store the time the user last logged in
to the secure server. Rules are in place to generate offenses if users
attempt to access the network in an unauthorized manner.

We would like to impose a business rule to expire a user's secure access if
they do not log in for a period of time. This time period is determined by
an external system.  
We would also like to generate a report showing the users that have secure
access, those that used to have it, but let it expire, and those that don't
have secure access in order to track who is using our systems.
