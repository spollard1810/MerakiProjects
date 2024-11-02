from netmiko import ConnectHandler
import csv
import re


USERNAME = ''
PASSWORD = ''
SECRET = ''

# Function to connect to Cisco device and retrieve running config for each interface on FEX
def get_running_config(device_hostname, csv_writer):
    # Define device parameters for Netmiko
    device_params = {
        'device_type': 'cisco_ios',
        'host': device_hostname,
        'username': USERNAME,
        'password': PASSWORD,
        'port': 22,  
        'secret': SECRET,  #enable password
        'verbose': True,
    }

    # Establish SSH connection
    try:
        net_connect = ConnectHandler(**device_params)
        net_connect.enable()  # Enter enable mode if required

        # Example command to get inventory (replace with actual command)
        output = net_connect.send_command('show inventory')

        # Parse inventory output to find FEX modules and their port counts dynamically
        fex_modules = parse_inventory(output)

        # Iterate through each FEX module
        for fex, num_interfaces in fex_modules.items():
            # Iterate through each interface on the FEX module
            for i in range(1, num_interfaces + 1):
                interface = f'Ethernet{fex}/1/{i}'  # Example interface format: Ethernet101/1/1

                # Get running config for the interface
                running_config = net_connect.send_command(f'show running-config interface {interface}')

                # Write the running config to CSV
                csv_writer.writerow({
                    'Hostname': device_hostname,
                    'Interface': interface,
                    'Running Config': running_config.strip()  # Remove extra whitespace
                })

                # Check if the interface belongs to a port channel
                port_channel = find_port_channel(net_connect, interface)
                if port_channel:
                    # Also write port channel information to CSV
                    csv_writer.writerow({
                        'Hostname': device_hostname,
                        'Interface': interface,
                        'Port Channel': port_channel
                    })

        net_connect.disconnect()

    except Exception as e:
        print(f"Error connecting to {device_hostname}: {str(e)}")

# Function to parse inventory output and extract FEX modules and their port counts
def parse_inventory(output):
    fex_modules = {}
    lines = output.splitlines()

    for line in lines:
        match = re.search(r'^FEX\s+(\d+).*?(\d+)\s+port', line)
        if match:
            fex_number = match.group(1)
            num_ports = int(match.group(2))
            fex_modules[fex_number] = num_ports

    return fex_modules

# Function to find if an interface belongs to a port channel
def find_port_channel(net_connect, interface):
    try:
        output = net_connect.send_command(f'show interface {interface} switchport')
        match = re.search(r'Port-channel (\d+) interface', output)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"Error finding port channel for {interface}: {str(e)}")
        return None

# Main function to read CSV and initiate processing
def main():
    with open('switches.csv') as csv_file, open('output.csv', 'w', newline='') as output_file:
        csv_reader = csv.DictReader(csv_file)
        fieldnames = ['Hostname', 'Interface', 'Running Config', 'Port Channel']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        devices = [row['hostname'] for row in csv_reader]

        for hostname in devices:
            print(f"Connecting to {hostname}...")
            get_running_config(hostname, csv_writer)
            print()

    print("Output saved to output.csv")

if __name__ == "__main__":
    main()
