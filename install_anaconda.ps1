# Set the URL for the Anaconda distribution page
$url = "https://repo.anaconda.com/archive/"

# Fetch the webpage
$page = Invoke-WebRequest -Uri $url

# Find the link to the latest Windows x86_64 Anaconda distribution
$installerUrlRelative = ($page.Links | Where-Object href -like "*Windows-x86_64.exe" | Select-Object -First 1).href

# Set the installer full url
$installerUrl = $url + $installerUrlRelative

# Set the installer name
$installerName = [System.IO.Path]::GetFileName($installerUrl)

# Download the installer
$start_time = Get-Date

Write-Host "Downloading $installerName..."
Invoke-WebRequest -Uri $installerUrl -OutFile $installerName |
    Out-Null

Write-Host "Time taken: $((Get-Date).Subtract($start_time).Seconds) second(s)"

# Install Anaconda
Start-Process -FilePath $installerName -ArgumentList '/InstallationType=JustMe /RegisterPython=0 /S /AddToPath=0 /D=%UserProfile%\Anaconda3'