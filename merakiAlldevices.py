#this script will pull in all devices from the Meraki network and write them to a csv file

# Import the necessary libraries
import os
import pandas as pd
import meraki


#Pregenerate a CSV with network ID and serial number
#csv should have header: name,model_id.name,serial_number
csvString = "name,model_id.name,serial_number,address\n"


#set working dir as the current filepath
os.chdir(os.path.dirname(__file__))

#instantiating the dashboard API
dashboard = meraki.DashboardAPI(api_key='')

#grabbing organizations
orgs = dashboard.organizations.getOrganizations()

#List of networks in the Organization
response = dashboard.organizations.getOrganizationNetworks(orgs[0]['id'])

for each in response:
    network_id = each['id']
    devices = dashboard.networks.getNetworkDevices(network_id)
    for device in devices:
        #using serial
        meraki_name = device['name']
        meraki_model = device['model']
        meraki_serial = device['serial']
        meraki_ip = device['lanIp']
        meraki_location = device['address']
        csvString += f"{meraki_name},{meraki_model},{meraki_serial},{meraki_ip}\n"

#writing to csv
with open('meraki.csv', 'w') as file:
    file.write(csvString)

