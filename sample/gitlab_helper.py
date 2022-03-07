import requests

gitlab_root_url = "https://git.ra1.intra.groupama.fr/api/v4"
# url du projet git contenant la conf des toggles
gitlab_conf_toggle_file_url = "/projects/6973/repository/files/version.json/raw?ref=master"
# url variabilisée pour récupérer un configmap d'un projet
gitlab_project_conf_file_url = "/projects/project_id/repository/files/.openshift%2Fenvironment%2Fproject_environment%2Fconfigmap.properties/raw?ref=version"
# url variabilisée pour récupérer un configmap d'un projet suricate
gitlab_suricate_conf_file_url = "/projects/project_id/repository/files/application-project_environment.yml/raw?ref=version"
# fonction de recherche d'un projet à partir de son nom
gitlab_search_url = "/projects?search=project_name&simple=true&membership=true"

# access token perso avec seulement les droits read_api, read_repository
headers = {'PRIVATE-TOKEN': 'BiG6CEXxiXyz6iomgBVW'}

ecli_suricate_project_id = "3971"


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


# Récupère la conf d'un projet pour un environnement et une version donnée
def get_suricate_configuration(environment, version):
    # FIXME faut il forcément chercher sur develop pour suricate ?
    project_url = gitlab_suricate_conf_file_url.replace("project_id", ecli_suricate_project_id).replace("project_environment", environment).replace(
        "version", "develop")
    # Certif auto signé donc verify à False
    result = requests.get(gitlab_root_url + project_url, verify=False, headers=headers)
    print(gitlab_root_url + project_url)
    print(result.text)
    return result.text


# Récupère le fichier de configuration de toggle pour une version donnée
def get_toggles(version):
    project_url = gitlab_conf_toggle_file_url.replace("version", version)
    print(project_url)
    # Certif auto signé donc verify à False
    return requests.get(gitlab_root_url + project_url, verify=False, headers=headers)