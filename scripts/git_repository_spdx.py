import requests
import base64
import pandas as pd

# Replace these variables with your GitHub details
GITHUB_TOKEN = 'your_github_token'  # Add your GitHub token here
REPO_OWNER = 'owner_name'  # Replace with the repository owner
REPO_NAME = 'repo_name'  # Replace with the repository name

# GitHub API base URL
GITHUB_API_URL = 'https://api.github.com'

def get_tags():
    """Fetches tags for the repository."""
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/tags"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch tags: {response.status_code}")
        return []

def get_license_for_tag(tag_sha):
    """Fetches the license information for a specific commit SHA."""
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/{tag_sha}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        tree = response.json().get('tree', [])
        for item in tree:
            if item['path'].lower() == 'license':
                license_url = item['url']
                license_response = requests.get(license_url, headers=headers)
                
                if license_response.status_code == 200:
                    license_data = license_response.json()
                    if 'content' in license_data:
                        # License content is base64 encoded; decode to get the license text
                        license_text = base64.b64decode(license_data['content']).decode('utf-8')
                        return license_text
    else:
        print(f"Failed to fetch license for SHA {tag_sha}: {response.status_code}")
    return None

def extract_spdx_expression(license_text):
    """Parses and extracts SPDX expression from the license text."""
    spdx_lines = [line for line in license_text.splitlines() if 'SPDX-License-Identifier:' in line]
    if spdx_lines:
        # Extract the SPDX identifier
        spdx_expression = spdx_lines[0].split('SPDX-License-Identifier:')[-1].strip()
        return spdx_expression
    return "No SPDX identifier found"

def extract_licenses():
    tags = get_tags()
    license_expressions = []
    
    for tag in tags:
        tag_name = tag['name']
        tag_sha = tag['commit']['sha']
        license_text = get_license_for_tag(tag_sha)
        
        if license_text:
            spdx_expression = extract_spdx_expression(license_text)
            license_expressions.append({
                'Tag': tag_name,
                'SPDX License Expression': spdx_expression
            })
        else:
            license_expressions.append({
                'Tag': tag_name,
                'SPDX License Expression': "No license file found"
            })
    
    # Convert results to DataFrame for display
    df = pd.DataFrame(license_expressions)
    return df

# Display the result in a DataFrame
license_df = extract_licenses()
license_df
