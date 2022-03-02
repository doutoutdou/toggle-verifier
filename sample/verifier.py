from datetime import datetime
# from flask import make_response, abort, jsonify
# import json
import datetime

from gitlab_helper import get_project_id, get_project_configuration

def verify_toggle():
    # conn = get_db_connection()

    # reservations = reservation_table()

    # class ReservationSchema(Schema):
    #     id = fields.Int()
    #     day = fields.Str()
    #     booked = fields.Bool()

    # request = reservations.select()
    # result = conn.execute(request)
    # conn.close
    #
    # schema = ReservationSchema(many=True)
    # jsonResult = schema.dump(result)
    toggles = {"CONF_TOGGLES_ITT_EVO_COURRIERS_ENABLED": "true", "CONF_TOGGLES_SYNTHESE_DEVIS_REFONTE_MUTUALISATION_SANTE_AUTO_MRH": "true"}
    print(toggles.items())
    print(toggles["CONF_TOGGLES_ITT_EVO_COURRIERS_ENABLED"])
    project_id = get_project_id("ecli-fo")
    configuration_iter = iter(get_project_configuration(project_id, "d", "develop").splitlines())
    for line in configuration_iter:
        if len(toggles) == 0:
            print("on arrete car on a vide le dictionnaire")
            break
        line_as_list = line.split("=")
        key = line_as_list[0]
        if toggles.__contains__(key):
            if toggles[key].casefold() == line_as_list[1].casefold():
                # print(key)
                toggles.__delitem__(key)


    # with configuration as file:
    #     for line in file:
    #         print(line)  # The comma to suppress the extra new line char
    return "toto", 200
