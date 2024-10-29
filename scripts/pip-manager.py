import requests
from datetime import datetime

# Package details
package_manager = "pip"
package_name = "flask"
package_version = "2.0.1"

# PyPI URL
pypi_url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"

# Make the request to PyPI API
response = requests.get(pypi_url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    license_info = data.get("info", {}).get("license", "No license info available")
    fetch_time = datetime.now().isoformat()

    # Display the license and fetch time
    print("License:", license_info)
    print("Fetch Time:", fetch_time)
else:
    print(f"Request to PyPI failed with status code {response.status_code}")
    print(response.text)