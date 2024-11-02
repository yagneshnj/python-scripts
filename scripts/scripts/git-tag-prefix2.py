import requests
import re

def get_matching_tag(repo_owner, repo_name, version, github_token):
    """
    Finds the best-matching tag in a GitHub repo for a given version by removing separators.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/tags"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        tags = response.json()
        
        # Normalize the input version by removing separators
        cleaned_version = re.sub(r"[\.\_\-]", "", version)
        
        for tag in tags:
            tag_name = tag.get('name', '')
            
            # Clean the tag name by removing separators
            cleaned_tag = re.sub(r"[\.\_\-]", "", tag_name)
            
            # Check if the cleaned tag matches the cleaned version
            if cleaned_tag == cleaned_version:
                return tag_name  # Return the original tag format if there's a match

        return f"No matching tag found for version {version}."

    except requests.RequestException as e:
        return f"An error occurred: {e}"

# Example usage
repo_owner = "junit-team"
repo_name = "junit5"
version = "5.0.7"  # The version we are trying to match
github_token = "ghp_your_github_token"  # Replace with your GitHub token

matching_tag = get_matching_tag(repo_owner, repo_name, version, github_token)
print(f"Matching Tag: {matching_tag}")
