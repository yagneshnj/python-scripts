import requests
from datetime import datetime

# Package details for NuGet
package_name = "Newtonsoft.Json"  # Example package name
version = "13.0.1"                # Example version

# NuGet API URL for package metadata
nuget_metadata_url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/{version}/{package_name.lower()}.nuspec"

# Make the request to fetch the NuSpec metadata file
response = requests.get(nuget_metadata_url)

# Check if the request was successful
if response.status_code == 200:
    nuspec_data = response.text
    # Extract license information from the metadata if available
    license_start = nuspec_data.find("<license")
    license_end = nuspec_data.find("</license>") + len("</license>")
    license_section = nuspec_data[license_start:license_end] if license_start != -1 else "No license info available in NuSpec."
    fetch_time = datetime.now().isoformat()

    # Display the license section and fetch time
    print("License Section:", license_section)
    print("Fetch Time:", fetch_time)
else:
    print(f"Failed to fetch NuSpec file with status code {response.status_code}")
    print(response.text)