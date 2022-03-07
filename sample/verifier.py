from distutils import util

from gitlab_helper import get_project_id, get_project_configuration, get_suricate_configuration, get_toggles
import yaml


def verify_toggle(toggle_tag):

    # récupération du fichier contenant les toggles pour la version indiquée
    projects_toggle_configuration = get_toggles(toggle_tag)
    # On suppose que si pas 200 alors c'est que le fichier n'a pas été trouvé, par exemple mauvais tag fourni
    if projects_toggle_configuration.status_code != 200:
        return "Fichier de toggle non trouvé pour le tag indiqué", 404
    # on crée un dict global qui contiendra en retour tous les toggles non trouvés
    global_toggle_dict = dict()
    for project in projects_toggle_configuration.json():
        project_name = project.get('projet')
        tag_version = project.get('tag')
        is_suricate_project = project.get('suricate')
        # Si le tag vaut develop, alors pas d'installation donc pas de vérification de toggle
        if tag_version == "develop":
            continue
        toggles = project.get('toggles')

        # on itère pour récupérer tous les toggles d'un projet
        toggle_dict_by_env = build_toggle_dict_by_env(toggles)
        project_id = get_project_id(project_name)
        # On a la liste de tous les toggles à vérifier pour un projet et tous les  environnements
        # on utilise list pour faire une copie, sinon on ne peut pas modifier le dictionnaire vu qu'on itère dessus
        for environment_key in list(toggle_dict_by_env.keys()):
            # Il ne faut pas procéder de la même facon si la conf est sur un repo suricate
            if is_suricate_project == "true":
                search_toggle_in_suricate_files(environment_key, tag_version, toggle_dict_by_env)
            else:
                search_toggle_in_configuration_files(environment_key, project_id, tag_version, toggle_dict_by_env)
        # si des toggles ne sont pas trouvés alors on ajoute pour les afficher en retour
        if len(toggle_dict_by_env) != 0:
            global_toggle_dict[project_name] = toggle_dict_by_env
    if len(global_toggle_dict) == 0:
        return "Tous les toggles sont OK", 200
    else:
        return global_toggle_dict, 206


# Construit un dict qui liste pour chaque envir la liste des toggles avec la valeur attendue
def build_toggle_dict_by_env(toggles):
    toggle_dict = dict()
    for toggle in toggles:
        for toggle_name in toggle.keys():
            # la clé est le nom du toggle
            # On récupère la liste des envirs pour un toggle
            for environment in toggle[toggle_name]:
                # pour chaque envir
                for environment_key in environment.keys():
                    # si l'envir n'est pas présent alors on ajoute
                    if environment_key not in toggle_dict:
                        env_dict = dict()
                        # on ajoute la clé à la liste des environnements pour ce projet
                        toggle_dict[environment_key] = env_dict
                    value_dict = dict()
                    # 2 cas possible, soit toggle simple et il y a juste une valeur
                    if isinstance(environment[environment_key], str):
                        value_dict["value"] = environment[environment_key]
                        toggle_dict[environment_key][toggle_name] = value_dict
                    else:
                        # soit toggle avec une strategy
                        toggle_dict[environment_key][toggle_name] = environment[environment_key]
    return toggle_dict


# Pour chaque environnement, chercher si les toggles présent dans le fichier de référence
# sont présents dans les fichiers environnement
def search_toggle_in_configuration_files(environment_key, project_id, tag_version, toggle_dict_by_env):
    toggle_list_by_env = toggle_dict_by_env[environment_key]
    # On récupère la conf des toggles sur GIT pour un projet & 1 envir donné
    project_configuration = get_project_configuration(project_id, environment_key, tag_version)
    for toggle_name, toggle_configuration in list(toggle_list_by_env.items()):
        # on reconstruit le toggle et sa valeur pour aller chercher dans le fichier de conf openshift ensuite
        # Pas de strategy pour un toggle qui n'est pas dans suricate
        toggle = toggle_name + "=" + toggle_configuration["value"]
        if project_configuration.find(toggle) != -1:
            # si -1 alors la clé n'a pas été trouvée dans le fichier
            del toggle_dict_by_env[environment_key][toggle_name]
    # si plus de toggle pour un environnement, alors on supprime l'environnement
    if len(toggle_dict_by_env[environment_key]) == 0:
        del toggle_dict_by_env[environment_key]


# Effectue la recherche des toggles dans suricate
def search_toggle_in_suricate_files(environment_key, tag_version, toggle_dict_by_env):
    toggle_list_by_env = toggle_dict_by_env[environment_key]
    # On récupère la conf des toggles sur GIT pour un projet & 1 envir donné
    project_configuration = yaml.load(get_suricate_configuration(environment_key, tag_version))
    toggles_from_suricate = project_configuration["oyster"]["toggles"]
    for toggle_name, toggle_configuration in list(toggle_list_by_env.items()):
        # FIXME, très moche de devoir faire ça, à améliorer
        # on a une liste de la forme {'name': 'contrat_affichageSuperDetailMRI', 'active': True}
        # et il faut regarder si la valeur de la clé name correspond à la clé du toggle présent dans la liste
        # Performance \o/
        for suricate_toggle in toggles_from_suricate:
            # On vérifie si le toggle du fichier suricate correspond au toggle attendu
            if suricate_toggle["name"].casefold() == toggle_name.casefold():
                # le toggle_configuration est un dict de la forme (si strategyParams)
                #  {'value': 'true', 'strategyParams': 'RENAULT,DACIA,GANAS,GEV,GPAT,GPREV,GPMA,NAT'}
                # le toggle provenant de suricate est par contre de la forme suivante
                # {'name': 'use-refm-for-marques', 'active': True, 'strategyParams': {'values': 'RENAULT,DACIA,GANAS,GEV,GPAT,GPREV,GPMA,NAT'}}
                if suricate_toggle["active"] == util.strtobool(toggle_configuration['value']):
                    # Si pas de strategyParams pour le toggle alors on peut supprimer
                    if "strategyParams" not in toggle_configuration:
                        del toggle_dict_by_env[environment_key][toggle_name]
                    else:
                        # On vérifie le format pour ne pas exploser en plein vol
                        if "values" in suricate_toggle["strategyParams"] and suricate_toggle["strategyParams"]["values"].casefold() == toggle_configuration["strategyParams"].casefold():
                            del toggle_dict_by_env[environment_key][toggle_name]
        # si plus de toggle pour un environnement, alors on supprime l'environnement
    if len(toggle_dict_by_env[environment_key]) == 0:
        del toggle_dict_by_env[environment_key]
