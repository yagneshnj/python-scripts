import requests

# ClearlyDefined API base URL
BASE_URL = "https://api.clearlydefined.io/definitions/maven/mavencentral"

# Example Maven packages with group, artifact, and version information
maven_packages = [
    {"group": "junit", "artifact": "junit", "version": "4.12"},
    {"group": "org.apache.commons", "artifact": "commons-lang3", "version": "3.12.0"}
]

# Function to fetch license information from ClearlyDefined
def fetch_discovered_license_expression(group, artifact, version):
    # Construct the ClearlyDefined API URL for the Maven package
    url = f"{BASE_URL}/{group}/{artifact}/{version}"
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
        print(f"Error fetching license for {artifact}:{version} - {e}")
        return "Error fetching license info"

# Main function to process all Maven packages
def get_maven_discovered_licenses(packages):
    licenses = {}
    for package in packages:
        group, artifact, version = package["group"], package["artifact"], package["version"]
        
        # Fetch discovered license expression from ClearlyDefined
        discovered_license_info = fetch_discovered_license_expression(group, artifact, version)
        licenses[f"{group}:{artifact}:{version}"] = discovered_license_info
    
    return licenses

# Fetch and display discovered licenses for all Maven packages
maven_discovered_licenses = get_maven_discovered_licenses(maven_packages)
for pkg, license_info in maven_discovered_licenses.items():
    print(f"Package: {pkg} - Discovered License Expression: {license_info}")
