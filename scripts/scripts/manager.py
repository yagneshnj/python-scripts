import requests

def get_package_info(package_manager, package_name, package_version):
    """
    Fetches the Git repository and license information for a specific package and version.
    Supports Maven, NPM, PyPi, and NuGet.
    """
    if package_manager.lower() == 'maven':
        return get_maven_info(package_name, package_version)
    elif package_manager.lower() == 'npm':
        return get_npm_info(package_name, package_version)
    elif package_manager.lower() == 'pypi':
        return get_pypi_info(package_name, package_version)
    elif package_manager.lower() == 'nuget':
        return get_nuget_info(package_name, package_version)
    else:
        return "Unsupported package manager."


def get_maven_info(package_name, package_version):
    """
    Fetches repository and license information for a Maven package.
    """
    group_id, artifact_id = package_name.split(":")
    url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{package_version}/{artifact_id}-{package_version}.pom"
    response = requests.get(url)
    if response.status_code == 200:
        # You can parse the XML file (pom.xml) here to get license and repository info
        pom_content = response.text
        return {"file_content": pom_content, "source": "pom.xml"}
    else:
        return "Package or version not found in Maven repository."


def get_npm_info(package_name, package_version):
    """
    Fetches repository and license information for an NPM package.
    """
    url = f"https://registry.npmjs.org/{package_name}/{package_version}"
    response = requests.get(url)
    if response.status_code == 200:
        package_data = response.json()
        repo_url = package_data.get("repository", {}).get("url", "No repository info available")
        license_info = package_data.get("license", "No license info available")
        return {
            "repository": repo_url,
            "license": license_info,
            "file_content": package_data,
            "source": "package.json"
        }
    else:
        return "Package or version not found in NPM registry."


def get_pypi_info(package_name, package_version):
    """
    Fetches repository and license information for a PyPi package.
    """
    url = f"https://pypi.org/pypi/{package_name}/{package_version}/json"
    response = requests.get(url)
    if response.status_code == 200:
        package_data = response.json()
        repo_url = package_data.get("info", {}).get("project_url", "No repository info available")
        license_info = package_data.get("info", {}).get("license", "No license info available")
        return {
            "repository": repo_url,
            "license": license_info,
            "file_content": package_data,
            "source": "pyproject.toml (if available)"
        }
    else:
        return "Package or version not found in PyPi registry."


def get_nuget_info(package_name, package_version):
    """
    Fetches repository and license information for a NuGet package.
    """
    url = f"https://api.nuget.org/v3-flatcontainer/{package_name}/{package_version}/{package_name}.nuspec"
    response = requests.get(url)
    if response.status_code == 200:
        # Parse XML if needed to extract license and repository information
        nuspec_content = response.text
        return {"file_content": nuspec_content, "source": ".nuspec file"}
    else:
        return "Package or version not found in NuGet registry."


# Example usage
package_manager = "npm"  # can be "maven", "npm", "pypi", or "nuget"
package_name = "express"  # Replace with the actual package name
package_version = "4.17.1"  # Replace with the actual package version

result = get_package_info(package_manager, package_name, package_version)
print(result)
