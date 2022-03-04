import json

import requests

gitlab_root_url = "https://git.ra1.intra.groupama.fr/api/v4"
gitlab_project_conf_file_url = "/projects/project_id/repository/files/.openshift%2Fenvironment%2Fproject_environment%2Fconfigmap.properties/raw?ref=version"
gitlab_conf_toggle_file_url = "/projects/6973/repository/files/version.json/raw?ref=master"
gitlab_search_url = "/search?scope=projects&search=project_name&simple=true&membership=true"

# access token perso avec seulement les droits read_api, read_repository
headers = {'PRIVATE-TOKEN': 'BiG6CEXxiXyz6iomgBVW'}


def get_gitlab_request():
    i = 0


# Récupère l'id git du projet à partir du name
def get_project_id(project_name):
    search_url = gitlab_search_url.replace("project_name", project_name)
    # Certif auto signé donc verify à False
    result = requests.get(gitlab_root_url + search_url, verify=False, headers=headers)
    # on récupère le json, on prend le 1er élément (2 projets ne peuvent pas avoir le même nom)
    # Puis on récupère via la clé
    return result.json()[0]['id']


# Récupère la conf d'un projet pour un environnement et une version donnée
def get_project_configuration(project_id, environment, version):
    project_url = gitlab_project_conf_file_url.replace("project_id", str(project_id)).replace("project_environment", environment).replace(
        "version", version)
    # Certif auto signé donc verify à False
    result = requests.get(gitlab_root_url + project_url, verify=False, headers=headers)
    return result.text


# Récupère le fichier de configuration de toggle pour une version donnée
def get_toggles(version):
    project_url = gitlab_conf_toggle_file_url.replace("version", version)
    print(project_url)
    # Certif auto signé donc verify à False
    result = requests.get(gitlab_root_url + project_url, verify=False, headers=headers)
    return result.json()