import requests

# Package details for npm
package_name = "express"
package_version = "4.17.1"

# npm Registry URL
npm_url = f"https://registry.npmjs.org/{package_name}/{package_version}"

# Make the request to npm registry
response = requests.get(npm_url)

if response.status_code == 200:
    data = response.json()
    repository_url = data.get("repository", {}).get("url", "")
    if "github.com" in repository_url:
        print("GitHub Repository URL:", repository_url)
    else:
        print("The repository is not hosted on GitHub or no repository URL found.")
else:
    print("Failed to retrieve package information from npm registry.")