import requests
from datetime import datetime
import xml.etree.ElementTree as ET

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
    # Parse the XML data
    root = ET.fromstring(nuspec_data)
    
    # Define the namespace
    namespace = {'ns': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}
    
    # Extract license information from the metadata if available
    license_start = nuspec_data.find("<license")
    license_end = nuspec_data.find("</license>") + len("</license>")
    license_section = nuspec_data[license_start:license_end] if license_start != -1 else "No license info available in NuSpec."
    
    # Extract the Git URL from the repository element
    repository_url = root.find('.//ns:repository', namespace)
    git_url = repository_url.get('url') if repository_url is not None else "No repository URL available in NuSpec."
    
    fetch_time = datetime.now().isoformat()

    # Display the license section, Git URL, and fetch time
    print("License Section:", license_section)
    print("Git Repository URL:", git_url)
    print("Fetch Time:", fetch_time)
else:
    print(f"Failed to fetch NuSpec file with status code {response.status_code}")
    print(response.text)
