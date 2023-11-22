"""
A script to scrape the latest pseudo dojo tables from GH using the API. 

At present we shall only focus on the repos with standard/stringent txt files
and ignore all others. This should give us PDv0.4 with SR and FR pseudos, with
psp8 files available for all of these. These parameters are hard coded into this 
file TODO move to a separate config file?

standard/stringent for each
ONCVPSP v0.4 FR LDA      - ONCVPSP-LDA-FR-PDv0.4
ONCVPSP v0.4 FR PBE      - ONCVPSP-PBE-FR-PDv0.4
ONCVPSP v0.4 FR PBESol   - ONCVPSP-PBESol-FR-PDv0.4
ONCVPSP v0.4 SR LDA      - ONCVPSP-LDA-PDv0.4
ONCVPSP v0.4 SR PBE      - ONCVPSP-PBE-PDv0.4
ONCVPSP v0.4 SR PBESol   - ONCVPSP-PBESol-PDv0.4

There is also 'ONCVPSP-PBE-SR-noCCv0.4' but will ignore that for now
"""

import os
import base64
import json
import requests
from collections import defaultdict

repos = ['ONCVPSP-LDA-FR-PDv0.4', 
        'ONCVPSP-LDA-PDv0.4', 
        'ONCVPSP-PBE-PDv0.4', 
        'ONCVPSP-PBEsol-PDv0.4', 
        'ONCVPSP-PBE-FR-PDv0.4', 
        'ONCVPSP-PBEsol-FR-PDv0.4']

def get_headers(github_token):
    headers = {'Authorization': f'token {github_token}'} if github_token else {}
    return headers

def get_repos(org_name, github_token):
    url = f"https://api.github.com/orgs/{org_name}/repos?sort=updated&direction=desc"
    headers = get_headers(github_token)
    repos = requests.get(url, headers=headers).json()
    
    return repos

def check_file_in_repo(repo_name, file_name, github_token):
    """
    Boolean to check that stringent.txt is in the repo
    """
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_name}"
    headers = get_headers(github_token)
    response = requests.get(url, headers=headers)
    
    return response.status_code == 200

def get_filepaths(repo_name, file_name, github_token):
    """
    Pull stringent/standard.txt from a single repo and return a dict 
    keyed by each element
    """
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_name}"
    headers = get_headers(github_token)
    response = requests.get(url, headers=headers)

    # TODO Raise an exception if missing stringent.txt?
    if response.status_code != 200:
        return {}  

    file_content = response.json()
    
    # Assuming the content is base64 encoded, decode it
    content = base64.b64decode(file_content['content']).decode('utf-8')

    filepaths_dict = {}
    
    for line in content.splitlines():
        parts = line.split('/')
        if len(parts) == 2:
            key, value = parts
            if key in filepaths_dict:
                filepaths_dict[key].append(value)
            else:
                filepaths_dict[key] = [value]

    return filepaths_dict

def get_djson(repo_name, file_name, github_token):
    """
    Pull stringent/standard.djson from a single repo and return a 
    dict keyed by each element including fpath, and hints
    """
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_name}"
    headers = get_headers(github_token)
    response = requests.get(url, headers=headers)

    # TODO Raise an exception if missing stringent.txt?
    if response.status_code != 200:
        return {}  

    file_content = response.json()
    
    # Assuming the content is base64 encoded, decode it
    content = json.loads(base64.b64decode(file_content['content']).decode('utf-8'))
    
    # print(content)
    
    table = content["pseudos_metadata"]

    return table


def get_relevant_repo_data(github_token):
    """
    Get all repos which contain a stringent.txt and return the filepaths keyed
    by the relevant elements as a list.
    
    TODO Temporarily hardcoded for ONCVPSPv0.4 will modify as we add more pseudos
    """
    print("Reading latest pseudo data")
    org_name = "PseudoDojo"

    # Get all repos 
    repos = get_repos(org_name, github_token)
    relevant_repos = defaultdict(dict)

    
    for repo in repos:
        short_name = repo['full_name'].split("/")[1]
        
        # TODO clean up repo so don't need workarounds?
        if "v0.4" not in short_name or "noCC" in short_name:
            continue
        
        print(short_name)
        
        # Get filepaths from each repo
        standard_djson = get_djson(repo['full_name'], "standard.djson", github_token)
        stringent_djson = get_djson(repo['full_name'], "stringent.djson", github_token)
        
        relativistic_type = "NC FR (ONCVPSP v0.4)" if "FR" in short_name else "NC SR (ONCVPSP v0.4)"
        xc_type = next((option for option in ["PBEsol", "PBE", "LDA"] if option in short_name), "none")
        
        relevant_repos[relativistic_type][xc_type] = {}
        
        # Add each repo with a dict storing the filepaths for each element
        relevant_repos[relativistic_type][xc_type]["standard"] = standard_djson
        relevant_repos[relativistic_type][xc_type]["stringent"] = stringent_djson

    return relevant_repos

if __name__ == "__main__":
    import os
    get_relevant_repo_data(os.environ.get('GITHUB_READONLY_TOKEN', 'default_token'))