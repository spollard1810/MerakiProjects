import csv
import os

# Get the current working directory
current_dir = os.getcwd()

# Define the input CSV file path
input_csv = os.path.join(current_dir, 'devices.csv')

# Initialize a list to hold the commands
commands = []

# Read the CSV file with UTF-8 encoding and handle BOM
with open(input_csv, mode='r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    # Print the headers to debug
    print("CSV Headers:", reader.fieldnames)

    for row in reader:
        # Accessing the columns safely
        obm = row.get('OBM')
        interface = row.get('Interface')
        leaf = row.get('Leaf')

        # Check if any of the values are None
        if obm is None or interface is None or leaf is None:
            print("Warning: One or more fields are missing in the row:", row)
            continue

        # Add the title for the commands
        commands.append(f"! Commands for {leaf}")
        commands.append(f"sh run interface mgmt0")
        commands.append("conf t")
        commands.append(f"interface mgmt0")
        commands.append("shutdown")
        commands.append("")  # Add a blank line for separation

# Define the output file path
output_file = os.path.join(current_dir, 'shutdown_commands.txt')

# Write commands to a file
with open(output_file, mode='w', encoding='utf-8') as file:
    for command in commands:
        file.write(command + "\n")

print(f"Commands have been written to {output_file}.")
