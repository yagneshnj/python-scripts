import requests
from datetime import datetime

# Package details
package_manager = "npm"
package_name = "express"
package_version = "4.17.1"

# npm Registry URL
npm_url = f"https://registry.npmjs.org/{package_name}/{package_version}"

# Make the request to npm registry
response = requests.get(npm_url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    license_info = data.get("license", "No license info available")
    fetch_time = datetime.now().isoformat()

    # Display the SPDX license and fetch time
    print("SPDX License:", license_info)
    print("Fetch Time:", fetch_time)
else:
    print(f"Request to npm registry failed with status code {response.status_code}")
    print(response.text)