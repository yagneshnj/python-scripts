import requests
import base64

def get_licenses_from_tag_and_repo(repo_owner, repo_name, tag, github_token):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get licenses at the specified tag
    licenses_at_tag = get_licenses_at_tag(repo_owner, repo_name, tag, headers)
    
    # Get license at the repository level
    license_at_repo = get_license_at_repo(repo_owner, repo_name, headers)
    
    # Return both licenses
    return {
        "licenses_at_tag": licenses_at_tag,
        "license_at_repo": license_at_repo
    }

def get_licenses_at_tag(repo_owner, repo_name, tag, headers):
    """
    Fetches the license contents from a specified tag in the GitHub repository.
    Returns a list of license names or contents if multiple are found.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees/{tag}?recursive=1"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tree = response.json().get("tree", [])

        # Find all potential license files
        license_files = [item for item in tree if "license" in item['path'].lower()]

        # If multiple license files are found, decode and return their contents
        licenses_content = []
        for license_file in license_files:
            license_url = license_file['url']
            license_response = requests.get(license_url, headers=headers)
            license_response.raise_for_status()
            license_content = license_response.json().get("content", "")
            decoded_content = base64.b64decode(license_content).decode("utf-8")
            licenses_content.append(decoded_content.splitlines()[0])  # First line as license name/identifier
            
        return licenses_content if licenses_content else ["No LICENSE file found at the specified tag."]
    
    except requests.RequestException as e:
        return [f"An error occurred while fetching licenses at tag: {e}"]

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
github_token = "mmm"  # Replace with your GitHub token

licenses = get_licenses_from_tag_and_repo(repo_owner, repo_name, tag, github_token)
print("Licenses at tag level:", licenses['licenses_at_tag'])
print("License at repo level:", licenses['license_at_repo'])
