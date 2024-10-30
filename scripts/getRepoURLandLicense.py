import requests

# GitHub access token
github_token = 'token'

# Package name to search for
package_name = "Newtonsoft.Json"  # Replace with your package name

# GitHub search API URL
github_search_url = "https://api.github.com/search/repositories"

# Search query to find repositories matching the package name
params = {
    "q": package_name,
    "sort": "stars",    # Sort by popularity to find the most likely match
    "order": "desc",
    "per_page": 1       # Limit results to the top 5 for review
}

# Set up headers with GitHub token
headers = {
    "Authorization": f"Bearer {github_token}"
}

# Make the request to GitHub API
response = requests.get(github_search_url, headers=headers, params=params)

if response.status_code == 200:
    search_results = response.json().get("items", [])

    # Check if any repositories were found
    if search_results:
        print("Potential GitHub Repositories Found:")
        for repo in search_results:
            repo_name = repo["full_name"]
            repo_url = repo["html_url"]
            print(f"Repository: {repo_name}")
            print(f"URL: {repo_url}")
            print("----")
    else:
        print("No GitHub repositories found matching the package name.")
else:
    print(f"Failed to search GitHub. Status code: {response.status_code}")
    print(response.text)

repository_url = repo_url

# Extract owner and repo name from the URL
if "github.com" in repository_url:
    parts = repository_url.strip().split("/")
    owner = parts[-2]
    repo = parts[-1]

    # GitHub API URL for license information
    github_api_url = f"https://api.github.com/repos/{owner}/{repo}/license"

    # Set up headers with the GitHub token
    headers = {
        "Authorization": f"Bearer {github_token}"
    }

    # Step 1: Get the primary license using the GitHub license API
    response = requests.get(github_api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        primary_license = data.get("license", {}).get("spdx_id", "No SPDX license info available")
        license_name = data.get("license", {}).get("name", "No license name available")

        print("Primary SPDX License:", primary_license)
        print("License Name:", license_name)

        # Step 2: Check for multiple license files in the root directory
        contents_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
        contents_response = requests.get(contents_url, headers=headers)

        if contents_response.status_code == 200:
            contents = contents_response.json()
            license_files = [file for file in contents if "license" in file["name"].lower()]

            if len(license_files) > 1:
                print("Multiple license files found:")
                for file in license_files:
                    print(" -", file["name"])
            elif len(license_files) == 1:
                print("Single license file found:", license_files[0]["name"])
            else:
                print("No license file found in the repository root.")
        else:
            print("Failed to retrieve repository contents.")
    else:
        print(f"Failed to retrieve primary license information from GitHub. Status code: {response.status_code}")
        print(response.text)
else:
    print("The repository URL is not hosted on GitHub.")

