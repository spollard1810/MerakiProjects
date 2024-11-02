###This script is intended to pull from Meraki API and compare from a CMDB csv export to check for any discrepancies between the two.###
import meraki
import csv
import jinja2
import os
import pandas as pd

#Pregenerate a CSV with network ID and serial number
#csv should have header: name,model_id.name,serial_number
csvString = "name,model_id.name,serial_number,Management Address\n"


#set working dir as the current filepath
os.chdir(os.path.dirname(__file__))

#instantiating the dashboard API
dashboard = meraki.DashboardAPI(api_key='')

#grabbing organizations
orgs = dashboard.organizations.getOrganizations()

#List of networks in the Organization
response = dashboard.organizations.getOrganizationNetworks(orgs[0]['id'])

#getting Networks in the organization returns JSON, so now we will list each network name from response
#for each instance of name in data returned, print the name
print('Networks in the organization:')
for name in response:
    print(name['name'])
    

#we will just list devices in output for now
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

#check to make sure meraki.csv was created
if os.path.exists('meraki.csv'):
    print("File created successfully") 
else:
    print("File not created")
    #shutdown the program
    exit()
    



