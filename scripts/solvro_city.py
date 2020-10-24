import json

def get_all_stops():
    # return 'works'
    with open("scripts/solvro_city.json", "r") as solvro_city_json:
        solvro_city = json.load(solvro_city_json)
    return solvro_city['nodes']