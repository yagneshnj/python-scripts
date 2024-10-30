import requests

# ClearlyDefined API base URL for NuGet packages
BASE_URL_NUGET = "https://api.clearlydefined.io/definitions/nuget/nuget/-/"

# Example NuGet packages with package name and version information
nuget_packages = [
    {"name": "Newtonsoft.Json", "version": "12.0.3"},
    {"name": "NLog", "version": "4.7.9"}
]

# Function to fetch discovered license expression from ClearlyDefined for NuGet
def fetch_discovered_license_expression_nuget(name, version):
    # Construct the ClearlyDefined API URL for the NuGet package
    url = f"{BASE_URL_NUGET}/{name}/{version}"
    print(f"Fetching license information from: {url}")
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print(data)  # Print the full response for debugging

        # Extract the discovered license expressions if available
        facets = data.get("licensed", {}).get("facets", {})
        discovered_licenses = facets.get("core", {}).get("discovered", {}).get("expressions", [])

        # Join the expressions with "AND" if there are multiple
        if discovered_licenses:
            return " AND ".join(discovered_licenses)
        else:
            return "No discovered license expression available"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching license for {name}:{version} - {e}")
        return "Error fetching license info"

# Main function to process all NuGet packages
def get_nuget_discovered_licenses(packages):
    licenses = {}
    for package in packages:
        name, version = package["name"], package["version"]
        
        # Fetch discovered license expression from ClearlyDefined for NuGet
        discovered_license_info = fetch_discovered_license_expression_nuget(name, version)
        licenses[f"{name}:{version}"] = discovered_license_info
    
    return licenses

# Fetch and display discovered licenses for all NuGet packages
nuget_discovered_licenses = get_nuget_discovered_licenses(nuget_packages)
for pkg, license_info in nuget_discovered_licenses.items():
    print(f"Package: {pkg} - Discovered License Expression: {license_info}")
