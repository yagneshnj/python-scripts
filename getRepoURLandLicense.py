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
