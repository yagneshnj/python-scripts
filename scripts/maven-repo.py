import requests
from xml.etree import ElementTree as ET

# Package details for Maven
group_id = "org.springframework"  # Example group ID
artifact_id = "spring-core"       # Example artifact ID
version = "5.3.9"                 # Example version

# Construct the Maven Central URL for the POM file
maven_pom_url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"

# Make the request to fetch the POM file
response = requests.get(maven_pom_url)

if response.status_code == 200:
    # Parse the POM XML content
    pom_data = response.content
    try:
        root = ET.fromstring(pom_data)

        # Try to find the repository URL in the <scm> section or <url> element
        repository_url = None
        scm = root.find(".//{http://maven.apache.org/POM/4.0.0}scm")
        if scm is not None:
            repository_url = scm.find("{http://maven.apache.org/POM/4.0.0}url")
            repository_url = repository_url.text if repository_url is not None else None
        else:
            project_url = root.find(".//{http://maven.apache.org/POM/4.0.0}url")
            repository_url = project_url.text if project_url is not None else None

        # Check if the repository URL is from GitHub
        if repository_url and "github.com" in repository_url:
            print("GitHub Repository URL:", repository_url)
        else:
            print("The repository is not hosted on GitHub or no repository URL found in the POM.")
    except ET.ParseError:
        print("Failed to parse the POM file.")
else:
    print(f"Failed to fetch POM file with status code {response.status_code}")
    print(response.text)