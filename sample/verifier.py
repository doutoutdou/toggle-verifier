from gitlab_helper import get_project_id, get_project_configuration, get_suricate_configuration, get_toggles


def verify_toggle(toggle_tag):

    # récupération du fichier contenant les toggles pour la version indiquée
    projects_toggle_configuration = get_toggles(toggle_tag)
    # On suppose que si pas 200 alors c'est que le fichier n'a pas été trouvé, par exemple mauvais tag fourni
    if projects_toggle_configuration.status_code != 200:
        return "Fichier de toggle non trouvé pour le tag indiqué", 404
    # on crée un dict global qui contiendra en retour tous les toggles non trouvés
    global_toggle_dict = dict()
    for projects in projects_toggle_configuration.json():
        project_name = projects.get('projet')
        tag_version = projects.get('tag')
        suricate = projects.get('suricate')
        # Si le tag vaut develop, alors pas d'installation donc pas de vérification de toggle
        if tag_version == "develop":
            continue
        toggles = projects.get('toggles')

        # on itère pour récupérer tous les toggles d'un projet
        toggle_dict = build_toggle_dict_by_env(toggles)

        project_id = get_project_id(project_name)
        # On a la liste de tous les toggles à vérifier pour un projet et tous les  environnements
        # on utilise list pour faire une copie, sinon on ne peut pas modifier le dictionnaire vu qu'on itère dessus
        for environment_key in list(toggle_dict.keys()):
            # FIXME voir pour les repos sur suricate ...
            toggle_list = toggle_dict[environment_key]

            # Il ne faut pas procéder de la même facon si la conf est sur un repo suricate
            if suricate == "true":
                search_toggle_in_suricate_configuration_files(environment_key, project_id, tag_version, toggle_dict, toggle_list)
            else:
                search_toggle_in_configuration_files(environment_key, project_id, tag_version, toggle_dict, toggle_list)

        # si des toggles ne sont pas trouvés alors on ajoute pour les afficher en retour
        if len(toggle_dict) != 0:
            global_toggle_dict[project_name] = toggle_dict
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
                    # on ajoute maintenant le toggle et sa valeur
                    toggle_dict[environment_key][toggle_name] = environment[environment_key]
    return toggle_dict


# Pour chaque environnement, chercher si les toggles présent dans le fichier de référence
# sont présents dans les fichiers environnement
def search_toggle_in_configuration_files(environment_key, project_id, tag_version, toggle_dict, toggle_list):
    # On récupère la conf des toggles sur GIT pour un projet & 1 envir donné
    project_configuration = get_project_configuration(project_id, environment_key, tag_version)
    for key, value in list(toggle_list.items()):
        # on reconstruit le toggle et sa valeur pour aller chercher dans le fichier de conf openshift ensuite
        toggle_with_value = key + "=" + value
        if project_configuration.find(toggle_with_value) != -1:
            # si -1 alors la clé n'a pas été trouvée dans le fichier
            del toggle_dict[environment_key][key]
    # si plus de toggle pour un environnement, alors on supprime l'environnement
    if len(toggle_dict[environment_key]) == 0:
        del toggle_dict[environment_key]


# Effectue la recherche des toggles dans suricate
def search_toggle_in_suricate_configuration_files(environment_key, project_id, tag_version, toggle_dict, toggle_list):
    # On récupère la conf des toggles sur GIT pour un projet & 1 envir donné
    project_configuration = get_suricate_configuration(environment_key, tag_version)
    # for key, value in list(toggle_list.items()):
    #     # on reconstruit le toggle et sa valeur pour aller chercher dans le fichier de conf openshift ensuite
    #     toggle_with_value = key + "=" + value
    #     if project_configuration.find(toggle_with_value) != -1:
    #         # si -1 alors la clé n'a pas été trouvée dans le fichier
    #         del toggle_dict[environment_key][key]
    # # si plus de toggle pour un environnement, alors on supprime l'environnement
    # if len(toggle_dict[environment_key]) == 0:
    #     del toggle_dict[environment_key]