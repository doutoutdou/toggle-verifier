import json
from datetime import datetime
# from flask import make_response, abort, jsonify
# import json
import datetime

from gitlab_helper import get_project_id, get_project_configuration, get_toggles


def verify_toggle(id):

    # récupération du fichier contenant les toggles pour la version
    projects_toggle_configuration = get_toggles(id)
    # on crée un dict global qui contiendra en retour tous les toggles non trouvés
    global_toggle_dict = dict()
    for projects in projects_toggle_configuration:
        project_name = projects.get('projet')
        tag_version = projects.get('tag')
        toggles = projects.get('toggles')
        toggle_dict = dict()
        # on itère pour récupérer tous les toggles d'un projet
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
        # On a la liste de tous les toggles à vérifier pour un projet et tous les  environnements
        # on utilise list pour faire une copie, sinon on ne peut pas modifier le dictionnaire vu qu'on itère dessus
        for environment_key in list(toggle_dict.keys()):
            # print(environment_key)
            # FIXME voir pour les repos sur suricate ...
            toggle_list = toggle_dict[environment_key]
            project_id = get_project_id(project_name)
            # On récupère la conf des toggles sur GIT pour un projet & 1 envir donné
            project_configuration = get_project_configuration(project_id, environment_key, tag_version)
            for key, value in list(toggle_list.items()):
                # print(key)
                # print(value)
                # on reconstruit le toggle et sa valeur pour aller chercher dans le fichier de conf ensuite
                toggle_with_value = key + "=" + value
                if project_configuration.find(toggle_with_value) != -1:
                    # si -1 alors la clé n'a pas été trouvée dans le fichier
                    # print("avant")
                    # print(toggle_dict[environment_key])
                    del toggle_dict[environment_key][key]
                    # print(toggle_dict[environment_key])
                    # print("apres")
            # si plus de toggle pour un environnement, alors on supprime
            print("longueur par envir")
            if len(toggle_dict[environment_key]) == 0:
                del toggle_dict[environment_key]
        # si des toggles ne sont pas trouvés alors on ajoute pour les afficher en retour
        if len(toggle_dict) != 0:
            # print("dict not empty")
            # print(toggle_dict)
            global_toggle_dict[project_name] = toggle_dict
    return global_toggle_dict
                # toggle_list[toggle_list_key]
                # print(toggle_list_key)
                # for toggle_key in toggle_list[toggle_list_key]:
                #     print(toggle_key)

                    # print(toggle_list)
            # for line in project_configuration:
            #     if len(toggle_list) == 0:
            #         print("on arrete car on a vide la liste des toggles à vérifier")
            #         break
            #     line_as_list = line.split("=")
            #     key = line_as_list[0]
            #     if toggles.__contains__(key):
            #         if toggle_list[key].casefold() == line_as_list[1].casefold():
            #             print(key)
                        # toggle_list.__delitem__(key)
            # print(toggle_list)
            # print("toggle_list_après")

        # print(toggle_dict)
        # print(env)
        # print("otot")
        # print(value)
        # i = 0
        # for keys in toggle.keys():
        # print(keys)

        # A VOIR => https://devstory.net/11437/python-dictionary
        # A VOIR => "https://www.programiz.com/python-programming/nested-dictionary"
        # for key, value in projects.items():
        #     if key == "projet":
        #         projet_name = value
        #     if key == "tag":
        #         tag_version = value
        #
        #     print(projet_name)
        #     print(tag_version)
        # for project in projects:
        #     print(project)
        # print(project["projet"])
        # print(project['tag'])
        # print(project['toggles'])
    # Print the type of data variable
    # print("Type:", type(toggles))
    # project_id = get_project_id("ecli-fo")
    # configuration_iter = iter(get_project_configuration(project_id, "d", "develop").splitlines())
    # for line in configuration_iter:
    #     if len(toggles) == 0:
    #         print("on arrete car on a vide le dictionnaire")
    #         break
    #     line_as_list = line.split("=")
    #     key = line_as_list[0]
    #     if toggles.__contains__(key):
    #         if toggles[key].casefold() == line_as_list[1].casefold():
    #             # print(key)
    #             toggles.__delitem__(key)

    # with configuration as file:
    #     for line in file:
    #         print(line)  # The comma to suppress the extra new line char
    # return "toto", 200
