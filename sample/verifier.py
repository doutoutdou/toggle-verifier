import json
from datetime import datetime
# from flask import make_response, abort, jsonify
# import json
import datetime

from gitlab_helper import get_project_id, get_project_configuration, get_toggles


def verify_toggle(id):

    toggles = {"CONF_TOGGLES_ITT_EVO_COURRIERS_ENABLED": "true",
               "CONF_TOGGLES_SYNTHESE_DEVIS_REFONTE_MUTUALISATION_SANTE_AUTO_MRH": "true"}
    # print(toggles.items())
    # print(toggles["CONF_TOGGLES_ITT_EVO_COURRIERS_ENABLED"])

    toggles = get_toggles(id)
    # print(toggles)
    for projects in toggles:
        project_name = projects.get('projet')
        tag_version = projects.get('tag')
        toggles = projects.get('toggles')
        # on itère pour récupérer tous les toggles d'un projet
        tab = {}
        print("toggles")
        print(toggles)
        for toggle in toggles:
            print("toggle")
            print(toggle)
            i = 0
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
    return "toto", 200
