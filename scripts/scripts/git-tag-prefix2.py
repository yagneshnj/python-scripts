import requests
import re
from collections import Counter

def analyze_tag_format(repo_owner, repo_name, github_token):
    """
    Analyzes the tag format in a GitHub repo to identify common patterns including prefixes, suffixes, and separators.
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

        patterns = []
        
        for tag in tags:
            tag_name = tag.get('name', '')
            
            # Match common prefix and suffix patterns around the version number
            match = re.match(r"^(?P<prefix>[\w]*)?(?P<separator>[-_.])?(?P<version>\d+([_.-]\d+)+)(?P<suffix>[\w]*)?$", tag_name)
            if match:
                prefix = match.group("prefix") or ""
                separator = match.group("separator") or "."
                suffix = match.group("suffix") or ""
                
                # Store each pattern as a tuple
                patterns.append((prefix, separator, suffix))

        # Find the most common prefix, separator, and suffix in the patterns
        most_common_prefix = Counter([p[0] for p in patterns]).most_common(1)[0][0]
        most_common_separator = Counter([p[1] for p in patterns]).most_common(1)[0][0]
        most_common_suffix = Counter([p[2] for p in patterns]).most_common(1)[0][0]

        return {
            "prefix": most_common_prefix,
            "separator": most_common_separator,
            "suffix": most_common_suffix
        }

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {"prefix": "", "separator": ".", "suffix": ""}

def format_version(version, repo_owner, repo_name, github_token):
    """
    Formats the version number based on the repo's common tag format.
    """
    # Analyze the tag pattern used in the repo
    format_info = analyze_tag_format(repo_owner, repo_name, github_token)

    # Replace dots in the version with the most common separator
    formatted_version = version.replace(".", format_info["separator"])

    # Add the common prefix and suffix
    return f"{format_info['prefix']}{formatted_version}{format_info['suffix']}"

# Example usage
repo_owner = "junit-team"
repo_name = "junit5"
version = "5.0.7"
github_token = "ghp_your_github_token"  # Replace with your GitHub token

formatted_version = format_version(version, repo_owner, repo_name, github_token)
print(f"Formatted Version: {formatted_version}")
