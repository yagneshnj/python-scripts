import requests
from datetime import datetime

# Package details for Maven
group_id = "org.springframework"  # Example group ID
artifact_id = "spring-core"       # Example artifact ID
version = "5.3.9"                 # Example version

# Construct Maven Central URL for the POM file
maven_pom_url = f"https://repo1.maven.org/maven2/{group_id.replace('.', '/')}/{artifact_id}/{version}/{artifact_id}-{version}.pom"

# Make the request to fetch the POM file
response = requests.get(maven_pom_url)

# Check if the request was successful
if response.status_code == 200:
    pom_data = response.text
    # Extract license information if available in the POM XML
    licenses_start = pom_data.find("<licenses>")
    licenses_end = pom_data.find("</licenses>") + len("</licenses>")
    licenses_section = pom_data[licenses_start:licenses_end] if licenses_start != -1 else "No license info available in POM."
    fetch_time = datetime.now().isoformat()

    # Display the license section and fetch time
    print("Licenses Section:", licenses_section)
    print("Fetch Time:", fetch_time)
else:
    print(f"Failed to fetch POM file with status code {response.status_code}")
    print(response.text)