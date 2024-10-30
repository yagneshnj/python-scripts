import requests

# ClearlyDefined API base URL
BASE_URL = "https://api.clearlydefined.io/definitions/maven/mavencentral"

# Example Maven packages with group, artifact, and version information
maven_packages = [
    {"group": "junit", "artifact": "junit", "version": "4.12"},
    {"group": "org.apache.commons", "artifact": "commons-lang3", "version": "3.12.0"}
]

# Function to fetch license information from ClearlyDefined
def fetch_license_from_clearlydefined(group, artifact, version):
    # Construct the ClearlyDefined API URL for the Maven package
    url = f"{BASE_URL}/{group}/{artifact}/{version}"
    print(f"Fetching URL: {url}")
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract the declared license
        declared_license = data.get("licensed", {}).get("declared", "No license info available")
        return declared_license

    except requests.exceptions.RequestException as e:
        print(f"Error fetching license for {artifact}:{version} - {e}")
        return "Error fetching license info"

# Main function to process all Maven packages
def get_maven_licenses(packages):
    licenses = {}
    for package in packages:
        group, artifact, version = package["group"], package["artifact"], package["version"]
        
        # Fetch license info from ClearlyDefined
        license_info = fetch_license_from_clearlydefined(group, artifact, version)
        licenses[f"{group}:{artifact}:{version}"] = license_info
    
    return licenses

# Fetch and display licenses for all Maven packages
maven_licenses = get_maven_licenses(maven_packages)
for pkg, license_info in maven_licenses.items():
    print(f"Package: {pkg} - License: {license_info}")
