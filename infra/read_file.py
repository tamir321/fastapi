import json
from business_logic import globals

with open('resources.data.json', 'r') as f:
    data = json.load(f)
    for req in data:
        globals.requests_list.append(req)