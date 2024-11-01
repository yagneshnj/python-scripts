import requests
import re
from collections import Counter

def get_tag_prefix(repo_owner, repo_name, github_token):
    """
    Fetches tags from a GitHub repo and determines the most common prefix format.

    Args:
        repo_owner (str): Owner of the GitHub repo.
        repo_name (str): Name of the GitHub repo.
        github_token (str): GitHub API token.

    Returns:
        str: The most common prefix (like 'v', 'r', or '').
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

        # Extract prefixes (e.g., 'v', 'r', or no prefix)
        prefixes = [re.match(r"^(v|r)?\d+", tag['name']).group(1) or '' for tag in tags if 'name' in tag]

        # Find the most common prefix
        most_common_prefix = Counter(prefixes).most_common(1)[0][0]
        return most_common_prefix

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return ""

def format_version(version, repo_owner, repo_name, github_token):
    """
    Formats the version number based on the repo's common tag prefix.

    Args:
        version (str): The base version number (e.g., "1.0.0").
        repo_owner (str): Owner of the GitHub repo.
        repo_name (str): Name of the GitHub repo.
        github_token (str): GitHub API token.

    Returns:
        str: The formatted version with the appropriate prefix.
    """
    # Get the most common prefix used in the repo's tags
    prefix = get_tag_prefix(repo_owner, repo_name, github_token)

    # Apply the prefix to the version
    return f"{prefix}{version}" if prefix else version

# Example usage
repo_owner = "junit-team"
repo_name = "junit5"
version = "1.0.0"
github_token = "lll"  # Replace with your GitHub token

formatted_version = format_version(version, repo_owner, repo_name, github_token)
print(f"Formatted Version: {formatted_version}")
