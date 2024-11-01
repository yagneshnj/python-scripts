import requests
import base64

def get_license_from_tag_and_repo(repo_owner, repo_name, tag, github_token):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get license at the specified tag
    license_at_tag = get_license_at_tag(repo_owner, repo_name, tag, headers)
    
    # Get license at the repository level
    license_at_repo = get_license_at_repo(repo_owner, repo_name, headers)
    
    # Return both licenses
    return {
        "license_at_tag": license_at_tag,
        "license_at_repo": license_at_repo
    }

def get_license_at_tag(repo_owner, repo_name, tag, headers):
    """
    Fetches the license content from a specified tag in the GitHub repository.
    """
    # GitHub API URL to get the tree structure for the specific tag
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{tag}?recursive=1"
    
    try:
        # Get the tree structure for the tag
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tree = response.json().get("tree", [])

        # Look for LICENSE or LICENSE.md file in the tree
        license_file = next((item for item in tree if item['path'].lower() in ['license', 'license.md']), None)
        
        if license_file:
            # Fetch the license file content using its URL
            license_url = license_file['url']
            license_response = requests.get(license_url, headers=headers)
            license_response.raise_for_status()
            license_content = license_response.json().get("content", "")
            
            # Decode base64 content
            decoded_content = base64.b64decode(license_content).decode("utf-8")
            return decoded_content.splitlines()[0]  # Return the first line as the license name
        else:
            return "No LICENSE file found at the specified tag."
    
    except requests.RequestException as e:
        return f"An error occurred while fetching the license at tag: {e}"

def get_license_at_repo(repo_owner, repo_name, headers):
    """
    Fetches the license information at the repository level.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/license"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        license_info = response.json()
        license_name = license_info.get("license", {}).get("name", "No license found at repo level.")
        return license_name
    except requests.RequestException as e:
        return f"An error occurred while fetching the license at repo level: {e}"

# Example usage
repo_owner = "junit-team"
repo_name = "junit5"
tag = "r5.10.5"
github_token = "kk"  # Replace with your GitHub token

licenses = get_license_from_tag_and_repo(repo_owner, repo_name, tag, github_token)
print(f"License at tag: {licenses['license_at_tag']}")
print(f"License at repo level: {licenses['license_at_repo']}")
