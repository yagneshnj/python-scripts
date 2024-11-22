import requests

def search_git_repository(package_name, ecosystem, github_token):
    """
    Search for a Git repository for a package using GitHub's search API.

    Args:
        package_name (str): Name of the package.
        ecosystem (str): Ecosystem ('maven', 'pypi', 'npm', 'nuget').
        github_token (str): GitHub personal access token.

    Returns:
        str: URL of the GitHub repository or an error message.
    """
    try:
        headers = {"Authorization": f"token {github_token}"}

        # Ecosystem-specific search queries
        if ecosystem == "maven":
            query = f"{package_name} filename:pom.xml"
        elif ecosystem == "pypi":
            query = f"{package_name} filename:setup.py"
        elif ecosystem == "npm":
            query = f"{package_name} filename:package.json"
        elif ecosystem == "nuget":
            query = f"{package_name} filename:*.csproj"
        else:
            return "Unsupported ecosystem. Supported: maven, pypi, npm, nuget."

        # GitHub API search endpoint
        url = f"https://api.github.com/search/code?q={query}&per_page=1"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Process results
        results = response.json()
        if results.get("total_count", 0) > 0:
            repo = results["items"][0]["repository"]["html_url"]
            return f"Repository found: {repo}"
        else:
            return "No repository found for the given package and ecosystem."

    except requests.RequestException as e:
        return f"Error during GitHub API request: {e}"


# Example usage
github_token = "your_github_personal_access_token"  # Replace with your GitHub token
print(search_git_repository("junit", "maven", github_token))
print(search_git_repository("flask", "pypi", github_token))
print(search_git_repository("react", "npm", github_token))
print(search_git_repository("Newtonsoft.Json", "nuget", github_token))
