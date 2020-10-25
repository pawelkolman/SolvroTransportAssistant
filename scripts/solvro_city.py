import json

# returns a json with all stops
def get_all_stops(path):
    solvro_city = json.load(open(path, 'r'))
    output = []
    for node in solvro_city['nodes']:
        output.append({'name':node['stop_name']})
    return json.dumps(output)