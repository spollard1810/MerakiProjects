# Define the working directory
$workingDir = Get-Location

# Import data.csv
$dataCSV = Import-Csv -Path "$workingDir\devices.csv"

# Import NNMI.csv
$nnmiCSV = Import-Csv -Path "$workingDir\nnmi.csv"

# Initialize an array to store entries not found in NNMI.csv
$notinNNMI = @()

$count = 0
# Loop through each entry in data.csv and compare with NNMI.csv
foreach ($entry in $dataCSV) {
    # Check if the hostname exists in NNMI.csv
    $nnmiEntry = $nnmiCSV | Where-Object { $_.Name -eq $entry.hostname }

    if ($nnmiEntry) {
        # Hostname exists in NNMI.csv, do nothing or log information if needed
        Write-Output "Hostname $($entry.hostname) exists in NNMI.csv"
    } else {
        # Hostname doesn't exist in NNMI.csv, add entry to notinNNMI array
        Write-Output "Hostname $($entry.hostname) does not exist in NNMI.csv"
        $notinNNMI += [PSCustomObject]@{
            Hostname = $entry.hostname
            IPAddress = $entry.IPAddress
            DeviceModel = $entry.DeviceModel
        }
    }
}

# Export the results to notinNNMINexus.csv
$notinNNMI | Export-Csv -Path "$workingDir\notinNNMINexus.csv" -NoTypeInformation

Write-Output "Comparison complete. Results exported to notinNNMINexus.csv"
