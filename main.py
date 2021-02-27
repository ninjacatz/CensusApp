import json
from UI.uifunctions import UIFunctions

# deserialize geojson files
with open("Choropleth/us_state_5m.json") as us_states_geojson_file:
    us_states = json.load(us_states_geojson_file)
with open("Choropleth/us_county_5m.json", encoding="latin1") as us_counties_geojson_file:
    us_counties = json.load(us_counties_geojson_file)
    
geojson_list = [us_states, us_counties]

# create UI
UIFunctions(geojson_list)

