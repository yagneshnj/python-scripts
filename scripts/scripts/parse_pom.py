import requests
import openai
import os

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure to set your API key as an environment variable

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


def parse_with_openai(file_content, file_type):
    """
    Uses OpenAI API to parse and extract repository and license information from a given file content.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an assistant parsing {file_type} files."},
                {"role": "user", "content": f"Extract repository URL and license information from this {file_type} content:\n\n{file_content}"}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error parsing with OpenAI: {e}"


def get_maven_info(package_name, package_version):
    """
    Fetches repository and license information for a Maven package and parses it using OpenAI API.
    """
    group_id, artifact_id = package_name.split(":")
    url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{package_version}/{artifact_id}-{package_version}.pom"
    response = requests.get(url)
    if response.status_code == 200:
        pom_content = response.text
        parsed_result = parse_with_openai(pom_content, "pom.xml")
        return {"parsed_data": parsed_result, "source": "pom.xml"}
    else:
        return "Package or version not found in Maven repository."


def get_nuget_info(package_name, package_version):
    """
    Fetches repository and license information for a NuGet package and parses it using OpenAI API.
    """
    url = f"https://api.nuget.org/v3-flatcontainer/{package_name}/{package_version}/{package_name}.nuspec"
    response = requests.get(url)
    if response.status_code == 200:
        nuspec_content = response.text
        parsed_result = parse_with_openai(nuspec_content, ".nuspec")
        return {"parsed_data": parsed_result, "source": ".nuspec file"}
    else:
        return "Package or version not found in NuGet repository."


# Example usage
package_manager = "maven"  # can be "maven", "npm", "pypi", or "nuget"
package_name = "org.apache.commons:commons-lang3"  # Replace with the actual package name
package_version = "3.12.0"  # Replace with the actual package version

result = get_package_info(package_manager, package_name, package_version)
print(result)
