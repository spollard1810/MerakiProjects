function Parse-DeviceData {
    param (
        [string]$fileName
    )

    $filePath = Join-Path -Path (Get-Location) -ChildPath $fileName

    if (-Not (Test-Path -Path $filePath)) {
        Write-Error "File not found: $filePath"
        return
    }

    $content = Get-Content -Path $filePath -Raw
    $blocks = $content -split "`r`n`r`n" | Where-Object { $_.Trim() -ne "" }
    $devices = @()

    foreach ($block in $blocks) {
        $lines = $block -split "`r`n" | Where-Object { $_.Trim() -ne "" }
        if ($lines.Count -eq 0) { continue }

        $device = [PSCustomObject]@{
            Hostname      = $null
            IPAddress     = $null
            SerialNumber  = $null
            DeviceModel   = $null
        }

        $hostnameAssigned = $false  # Track if hostname has been assigned

        foreach ($line in $lines) {
            if ($line -match '^\d{1,3}(\.\d{1,3}){3}$') {
                $device.IPAddress = $line
            }
            elseif ($line -match '^[A-Z0-9]{11}$') {
                $device.SerialNumber = $line
            }
            elseif ($line -match 'n9k') {
                $device.DeviceModel = $line
            }
            elseif ($line -match '^[a-zA-Z0-9\-]{12,}$' -and $line -match '-.*-.+' -and -Not ($line -match '^n') -and -Not $hostnameAssigned) {
                $device.Hostname = $line
                $hostnameAssigned = $true  # Set the flag to true
            }
        }

        if ($device.Hostname -or $device.IPAddress -or $device.SerialNumber -or $device.DeviceModel) {
            $devices += $device
        }
    }

    return $devices
}

# Example usage
$devices = Parse-DeviceData -fileName 'devices.txt'

Write-Host "Number of devices: $($devices.Count)"

foreach ($device in $devices) {
    Write-Output "Device Object: $($device | ConvertTo-Json -Depth 5)"
}

$csvPath = Join-Path -Path (Get-Location) -ChildPath 'devices.csv'
$devices | Export-Csv -Path $csvPath -NoTypeInformation

Write-Host "Data has been exported to: $csvPath"
