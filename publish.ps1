# Define the list of files to copy
$files = @(
    'cytoBand.txt',
    'genexusPgtAEndpoint.wsgi',
    'requirements.txt',
    'vcf_functions.py',
    'app.py'
)

# Set the current date in the format you specified
$dateStr = (Get-Date -Format "yyyy-MM-dd")

# Set the destination zip file name
$zipFileName = "genexusPgtAEndpoint_deploy_$dateStr.zip"

# Check if zip file already exists and remove it to ensure a clean start
if (Test-Path $zipFileName) {
    Remove-Item -Path $zipFileName -Force
}

# Copy each file into the zip archive
foreach ($file in $files) {
    if (Test-Path $file) {
        Compress-Archive -LiteralPath $file -Update -DestinationPath $zipFileName
    } else {
        Write-Host "WARNING: File $file does not exist in the script's root directory."
    }
}

Write-Host "Deployment completed. Check $zipFileName."