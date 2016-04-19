This repository contains samples for the `system/servers` endpoint of the API.

These samples are provided for reference purposes on an "as is" basis, and are without warranties of any kind.

It is strongly advised that these samples are not run against production systems.

Any issues discovered using the samples should not be directed to QRadar support, but be reported on the Github issues tracker.

# Servers Samples

Scripts in this directory demonstrate how to use the `/system/servers`
endpoints of the API.


For a list of the endpoints that you can use along with the parameters
they accept you can view the REST API interactive help page at
`https://<hostname>/api_doc`  
You can also retrieve a list of available endpoints through the api itself
at the `/api/help/capabilities` endpoint.

### 01_servers.py
In this sample you will see how to retrieve a list of the server hosts in the 
QRadar deployment and how the general settings of each server hosts can be 
retrieved and updated using the REST API. Currently, we only support updating 
the email server address of a server through the endpoint.  


### 02_firewallRules.py
In this sample you will see how the access control firewall rules of each 
server host can be retrieved and updated using the REST API. Access control 
firewall rules are the custom iptable accepting rules defined by the users 
and are different from the default iptable rules used by the QRadar system.  
Updating the access control firewall rules won't affact the default rules in 
QRadar deployment.  The example shows how to add a new rule to open a new 
port on each managed host. Note: setting the new rules will override the old
existing rules.

 
### 03_ethernetNetworkInterfaces.py
In this sample you will see how the settings of an ethernet network interfaces
on a server host can be retrieved and updated using the REST API. Note: only 
non-management and non-HACrossover interfaces are allowed to be updated. 


### 04_bondedNetworkInterfaces.py
In this sample you will see how to create a bonded interface on the top of 
existing ethernet network interfaces and how to update the settings (IP, 
netmask, slave interfaces, etc) of an existing bonded interface.  
existing bonded network interface. ALso it shows you how to unbond (remove) 
an existing bonded interface and recover its slave interfaces to individual 
ethernet interfaces which will be in monitor state after unbond.   