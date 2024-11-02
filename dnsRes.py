##This script will grab DNS of each switch on the Meraki network, and write it to a csv file hostname, DNS

import meraki
import csv
import os
import pandas as pd
#Pregenerate a CSV with name, DNS
#csv should have header: name,model_id.name,serial_number

#instantiating the dashboard API
dashboard = meraki.DashboardAPI(api_key='')

#grabbing organizations
orgs = dashboard.organizations.getOrganizations()


#loading in meraki.csv with loaded data

os.chdir(os.path.dirname(__file__))

# Verify the existence of 'missing.csv' and 'nnmi.csv'
if not (os.path.exists('meraki.csv')):
    print("Error: 'meraki.csv' not found.")
    exit()
    
merakidf = pd.read_csv('meraki.csv')

#creating data struct which will hold each device that has a model_id.name of beginning with 'MS'
devices = []
for index, row in merakidf.iterrows():
    if row['model_id.name'].startswith('MS'):
        devices.append(row)
print(devices)
print(devices.count)

#creating csv file 'DNSentries.csv'
#headers are 'hostname, serial number, and DNS'
with open('DNSentries.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['hostname', 'serial number', 'DNS1', 'DNS2'])
#now using dashboard API to grab DNS from each switch
for device in devices:
    #grabbing the DNS from the switch
    dns = dashboard.devices.getDeviceManagementInterface(device['serial_number'])
    #try to grab 'staticDns' from the dictionary, ['wan1']['staticDns']
    try:
        dnsEntry = dns['wan1']['staticDns']
    except:
        print("No DNS found")
        dnsEntry = ['No DNS found', 'No DNS found']
        continue
    dns1 = dnsEntry[0]
    dns2 = dnsEntry[1]

    #writing to the csv file
    with open('DNSentries.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([device['name'], device['serial_number'], dns1, dns2])
    #resetting the dns values to None
    dns1 = None
    dns2 = None
    

#iterating through meraki