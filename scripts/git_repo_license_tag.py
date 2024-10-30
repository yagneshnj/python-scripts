import requests

def get_license_for_repo_tag(owner, repo, tag, github_token):
    # GitHub API URL to fetch tags
    tags_url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    
    # Fetch all tags to get the commit SHA for the specified tag
    response = requests.get(tags_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch tags: {response.json().get('message')}")
    
    tags = response.json()
    tag_commit_sha = None
    for tag_data in tags:
        if tag_data['name'] == tag:
            tag_commit_sha = tag_data['commit']['sha']
            break
    
    if not tag_commit_sha:
        raise Exception(f"Tag '{tag}' not found in repository '{owner}/{repo}'")

    # GitHub API URL to fetch the license information for a specific commit
    license_url = f"https://api.github.com/repos/{owner}/{repo}/contents/LICENSE?ref={tag_commit_sha}"
    
    # Fetch the license content at the tag's commit SHA
    license_response = requests.get(license_url, headers=headers)
    if license_response.status_code != 200:
        raise Exception(f"Failed to fetch license: {license_response.json().get('message')}")
    
    license_data = license_response.json()
    
    # Decode the license content if needed (it's base64 encoded)
    license_content = license_data['content']
    license_decoded = requests.utils.unquote(license_content).decode('utf-8')
    
    return {
        "license_name": license_data.get("license", {}).get("name"),
        "license_content": license_decoded
    }

# Example usage
owner = "tomoh1r"
repo = "ansible-vault"
tag = "v1.2.0"
github_token = "repo"  # Make sure your token has repo access

license_info = get_license_for_repo_tag(owner, repo, tag, github_token)
print("License Name:", license_info["license_name"])
print("License Content:", license_info["license_content"])
