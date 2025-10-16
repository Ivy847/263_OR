import numpy as np
import pandas as pd

def generate_saturday_demand(stores, demand_limits):
    saturday_demand_dict = {}
    for store in stores:
        demand = round(numpy.random.uniform(low=0.0, high=demand_limits[store], size=None))
        if demand != 0:
            saturday_demand_dict[store] = demand

    return saturday_demand_dict

def bootstrap_weekday_demand(store_demands):
    weekday_demand_dict = {}
    for store in store_demands:
        weekday_demand_dict[store] = numpy.random.choice(store_demands[store])

    return weekday_demand_dict

def find_duration_simulation(tours, duration_data, index, demand_total):
    '''
    Parameters:
    tours: str array containing routes to evaluate for duration
    duration_data: pandas dataframe containing durations between each node
    index: dictionary with node names as keys, to access durations from duration_data
    demand_total: array containing total demand, ordered correspondingly to tours
    '''
    duration = np.zeros(len(tours))
    tour_number = 0
    for tour in tours:
        nodes = tour.split('->')
        route_demand = demand_total[tour_number]
        prev = "CentrePort Wellington"
        for node in nodes:
            prev_index = index[prev]
            node_index = index[node]
            duration[tour_number] += duration_data.iloc[prev_index, node_index + 1]
            prev = node
        duration[tour_number] += 15 * 60 * route_demand
        tour_number += 1
    return duration


ORSkey = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImEwMGM2OGNiZTE1NzQzZTBiM2MyY2U0NDdmZGVhMmU0IiwiaCI6Im11cm11cjY0In0='
import numpy as np
import pandas as pd
locations = pd.read_csv("WoolworthsLocations.csv")
import openrouteservice as ors

# Boot up client to OpenRouteService. ORSkey is your own key as a string.
client = ors.Client(key=ORSkey)
coords = locations[['Long', 'Lat']] # Mapping packages work with Long, Lat arrays
coords = coords.to_numpy().tolist() # Make the arrays into a list of lists.

#creates martrix of durations between points
matrix = client.distance_matrix(
    locations=coords,
    profile='driving-hgv',
    metrics=['duration'],
    validate=False,
)
names = locations["Store"].tolist() # creates list of names 
# Creates dataframe of durations with the store names
durations = pd.DataFrame(matrix['durations'], index=names, columns=names)
mean = 1.374
sigma = 0.116
low = 1
high = 2

sigma2 = np.log(1 + (sigma**2)/(mean**2))
sigma  = np.sqrt(sigma2)
mu     = np.log(mean) - 0.5*sigma2

rng = np.random.default_rng()  # sets random seed

multiplier_matrix = rng.lognormal(mean=mu, sigma=sigma, size=durations.shape) # creates a matrix with random mulitplers
multiplier_matrix = np.clip(multiplier_matrix, low, high) # makes sure no values go over or under the max and min

var_durations = pd.DataFrame(durations.to_numpy() * multiplier_matrix, index=durations.index, columns=durations.columns)

print(var_durations)

routes = [
    ["Woolworths Porirua", "Woolworths Johnsonville"],
    ["Woolworths Upper Hutt", "Woolworths Maidstone"],
    ["Metro Cable Car Lane", "Woolworths Karori", "Woolworths Crofton Downs"],
    ["Woolworths Kilbirnie", "Woolworths Newtown", "FreshChoice Cuba Street"],
    ["Woolworths Petone", "Woolworths Wainuiomata", "FreshChoice Woburn"],
    ["Woolworths Johnsonville Mall", "Woolworths Queensgate", "Woolworths Lower Hutt"],
    ["Woolworths Aotea", "FreshChoice Cannons Creek", "Woolworths Tawa"]
]

demands = bootstrap_weekday_demand(weekday_demand_distribution)

route_demand_dict_working = {}
route_demand_dict_not_working = {}

for route in routes:
    total_demand = 0
    for store in route:
        total_demand += demands[store]
    # make the route name a simple string (normal dict key)
    route_name = " ->".join(route)
    if total_demand <= 9:
        route_demand_dict_working[route_name] = total_demand
    else:
        route_demand_dict_not_working[route_name] = total_demand

print(route_demand_dict_working)
print(route_demand_dict_not_working)




