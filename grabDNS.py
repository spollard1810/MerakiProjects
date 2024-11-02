##This script will grab DNS of each switch on the Meraki network, and write it to a csv file hostname, DNS

import meraki
import csv
#Pregenerate a CSV with name, DNS
#csv should have header: name,model_id.name,serial_number
csvString = "name,model_id.name,serial_number\n"

#instantiating the dashboard API
dashboard = meraki.DashboardAPI(api_key='API_KEY')

#grabbing organizations
orgs = dashboard.organizations.getOrganizations()

#List of networks in the Organization
org = dashboard.organizations.getOrganizationNetworks(orgs[0]['id'])

print(response)

#get all devices in the org; only with model 'ms'

for each in response:
    network_id = each['id']
    devices = dashboard.networks.getNetworkDevices(network_id)
    for device in devices:
        #if 'ms' is in model string then print name, serial, model
        if device['model'].find('ms') != -1:
            print(device['name'] + " " + device['serial']) + " " + device['model'] + " " + dashboard.devices.getDeviceManagementInterface(device['serial'])


    
    