# Import the CSV file
$workingDir = Get-Location
$devices = Import-Csv -Path "$workingDir\devices.csv"
$cmdb = Import-Csv -Path "$workingDir\cmdb_ci_netgear.csv"

# Initialize object array for devices not found in CMDB
$deviceArray = @()

# Initialize counters
$countFound = 0
$countNotFound = 0

# Loop through each device in devices.csv
foreach ($device in $devices) {
    # Check if SerialNumber exists in cmdb_ci_netgear.csv as serial_number
    Write-Output "Searching for Serial Number $($device.SerialNumber) in cmdb_ci_netgear.csv"
    $cmdbEntry = $cmdb | Where-Object { $_.serial_number -eq $device.SerialNumber }

    # If serial number exists in cmdb_ci_netgear.csv
    if ($cmdbEntry) {
        # SerialNumber exists in cmdb_ci_netgear.csv
        Write-Output "Serial Number $($device.SerialNumber) exists in cmdb_ci_netgear.csv"
        $countFound++
    } else {
        # SerialNumber doesn't exist in cmdb_ci_netgear.csv, add entry to deviceArray
        Write-Output "Serial Number $($device.SerialNumber) does not exist in cmdb_ci_netgear.csv"
        
        # Create a new object for each device not found
        $deviceObj = [PSCustomObject]@{
            Hostname      = $device.Hostname
            IPAddress     = $device.IPAddress
            SerialNumber  = $device.SerialNumber
            DeviceModel   = $device.DeviceModel
        }
        $deviceArray += $deviceObj
        $countNotFound++
    }
}

# Output devices not found in cmdb_ci_netgear.csv
if ($deviceArray.Count -gt 0) {
    Write-Host "Devices not found in cmdb_ci_netgear.csv:"
    $deviceArray | Format-Table
    Write-Host "Total devices not found: $($countNotFound)"
} else {
    Write-Host "All devices found in cmdb_ci_netgear.csv"
}

Write-Host "Total devices found in CMDB: $($countFound)"

# Export the results to notinCMDB.csv
$deviceArray | Export-Csv -Path "$workingDir\notinCMDB.csv" -NoTypeInformation
