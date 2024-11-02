###This script is intended to pull from Meraki API and compare from a CMDB csv export to check for any discrepancies between the two.###
import meraki
import csv
import jinja2
import os
import pandas as pd

#Pregenerate a CSV with network ID and serial number
#csv should have header: name,model_id.name,serial_number
csvString = "name,model_id.name,serial_number,ip_address\n"


#set working dir as the current filepath
os.chdir(os.path.dirname(__file__))

#instantiating the dashboard API
dashboard = meraki.DashboardAPI(api_key='YOUR_API_KEY')

#grabbing organizations
orgs = dashboard.organizations.getOrganizations()

#List of networks in the Organization
response = dashboard.organizations.getOrganizationNetworks(orgs[0]['id'])

counter = 0

for each in response:
    network_id = each['id']
    devices = dashboard.networks.getNetworkDevices(network_id)
    for device in devices:
        #if device model has 'ms' in it, it is a switch, we will only include switches in the csv
        if 'ms' in device['model']:
            meraki_name = device['name']
            meraki_model = device['model']
            meraki_serial = device['serial']
            meraki_ip = device['lanIp']
            meraki_location = device['address']
            csvString += f"{meraki_name},{meraki_model},{meraki_serial},{meraki_ip}\n"
            counter+=1
            #using serial
            



print(f"Total switches found: {counter}")
#writing to csv
with open('meraki.csv', 'w') as file:
    file.write(csvString)