import requests
from xml.etree import ElementTree as ET

# NuGet package name
package_name = "Newtonsoft.Json"  # Example package name

# NuGet API URL for latest version metadata
nuget_url = f"https://api.nuget.org/v3/registration5-semver1/{package_name.lower()}/index.json"

# Make the request to NuGet API
response = requests.get(nuget_url)

if response.status_code == 200:
    data = response.json()

    # Get the latest package entry
    latest_entry = data.get("items", [{}])[-1].get("items", [{}])[-1]

    # Retrieve the repository URL from the catalog entry
    repository_url = latest_entry.get("catalogEntry", {}).get("projectUrl", None)

    if repository_url and "github.com" in repository_url:
        print("GitHub Repository URL:", repository_url)
    elif repository_url:
        print("Repository URL:", repository_url)
    else:
        print("No repository URL found for the specified NuGet package.")
else:
    print(f"Request to NuGet API failed with status code {response.status_code}")
    print(response.text)