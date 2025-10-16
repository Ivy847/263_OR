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
            duration[tour_number] += duration_data.iloc[prev_index, node_index]
            prev = node
        duration[tour_number] += 15 * 60 * route_demand
        tour_number += 1
    return duration

index = {
        "Woolworths Aotea" : 0,
        "Woolworths Crofton Downs" : 1,
        "Woolworths Johnsonville" : 2,
        "Woolworths Johnsonville Mall" : 3,
        "Woolworths Karori" : 4,
        "Woolworths Kilbirnie" : 5,
        "Woolworths Lower Hutt" : 6,
        "Woolworths Maidstone" : 7,
        "Woolworths Newtown" : 8,
        "Woolworths Petone" : 9,
        "Woolworths Porirua" : 10,
        "Woolworths Queensgate" : 11,
        "Woolworths Tawa" : 12,
        "Woolworths Upper Hutt" : 13,
        "Woolworths Wainuiomata" : 14,
        "FreshChoice Cuba Street" : 15,
        "FreshChoice Woburn" : 16,
        "FreshChoice Cannons Creek" : 17,
        "Metro Cable Car Lane" : 18,
        "CentrePort Wellington" : 19,
    }

weekend_demand_limits = {
        "FreshChoice Cannons Creek" : 3,
        "FreshChoice Cuba Street" : 2,
        "FreshChoice Woburn" : 2,
        "Metro Cable Car Lane" : 2,
        "Woolworths Aotea" : 3,
        "Woolworths Crofton Downs" : 4,
        "Woolworths Johnsonville" : 4,
        "Woolworths Johnsonville Mall" : 3,
        "Woolworths Karori" : 3,
        "Woolworths Kilbirnie" : 3,
        "Woolworths Lower Hutt" : 3,
        "Woolworths Maidstone" : 4,
        "Woolworths Newtown" : 3,
        "Woolworths Petone" : 3,
        "Woolworths Porirua" : 4,
        "Woolworths Queensgate" : 3,
        "Woolworths Tawa" : 2,
        "Woolworths Upper Hutt" : 3,
        "Woolworths Wainuiomata" : 4,
        "CentrePort Wellington" : 0,
    }

weekday_demand_distribution = {
        "FreshChoice Cannons Creek" : [3,2,2,2,1,1,1,2,1,2,3,3,3,3,4,1,1,1,2,1],
        "FreshChoice Cuba Street" : [1,2,2,1,2,3,2,1,2,1,1,2,2,2,2,2,2,3,2,2],
        "FreshChoice Woburn" : [2,2,3,1,1,2,2,1,1,1,3,2,3,1,2,1,2,1,1,2],
        "Metro Cable Car Lane" : [2,2,1,2,2,1,1,2,1,2,5,1,2,3,2,2,1,2,2,3],
        "Woolworths Aotea" : [2,5,3,2,3,2,3,2,3,2,3,3,3,2,2,1,3,1,2,1],
        "Woolworths Crofton Downs" : [3,2,4,2,3,1,4,4,6,2,5,2,4,3,2,1,2,2,1,2],
        "Woolworths Johnsonville" : [3,1,2,5,3,2,5,4,3,5,5,2,1,3,3,1,2,4,3,1],
        "Woolworths Johnsonville Mall" : [2,3,4,2,3,2,3,2,1,2,1,3,1,1,4,2,1,5,1,2],
        "Woolworths Karori" : [2,2,3,2,3,3,2,1,2,3,3,2,4,3,3,3,2,1,2,2],
        "Woolworths Kilbirnie" : [2,3,4,2,2,1,2,4,3,1,2,2,2,2,3,2,3,3,3,4],
        "Woolworths Lower Hutt" : [2,2,1,4,1,1,2,3,2,2,3,3,5,3,1,3,3,2,2,3],
        "Woolworths Maidstone" : [3,4,2,2,2,3,5,4,3,6,2,2,2,2,1,1,1,6,3,3],
        "Woolworths Newtown" : [2,4,2,5,3,3,3,5,3,2,4,1,2,3,3,1,1,3,2,3],
        "Woolworths Petone" : [3,5,2,2,4,1,2,2,2,3,3,3,2,2,1,2,3,2,3,2],
        "Woolworths Porirua" : [5,1,5,2,2,3,2,4,1,3,3,3,3,5,2,2,2,2,4,1],
        "Woolworths Queensgate" : [2,2,3,3,4,2,2,2,2,1,2,1,4,2,2,1,2,3,1,2,4,2,2],
        "Woolworths Tawa" : [2,2,2,2,2,1,1,1,1,4,2,2,1,2,3,1,2,4,2,2],
        "Woolworths Upper Hutt" : [2,1,2,1,1,1,2,1,1,4,3,2,4,3,2,4,1,3,2,2],
        "Woolworths Wainuiomata" : [3,4,2,2,2,2,2,3,3,3,1,3,2,4,2,4,5,1,1,5],
        "CentrePort Wellington" : [0],
    }

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
    ["CentrePort Wellington","Woolworths Porirua", "Woolworths Johnsonville","CentrePort Wellington"],
    ["CentrePort Wellington","Woolworths Upper Hutt", "Woolworths Maidstone","CentrePort Wellington"],
    ["CentrePort Wellington","Metro Cable Car Lane", "Woolworths Karori", "Woolworths Crofton Downs","CentrePort Wellington"],
    ["CentrePort Wellington","Woolworths Kilbirnie", "Woolworths Newtown", "FreshChoice Cuba Street","CentrePort Wellington"],
    ["CentrePort Wellington","Woolworths Petone", "Woolworths Wainuiomata", "FreshChoice Woburn","CentrePort Wellington"],
    ["CentrePort Wellington","Woolworths Johnsonville Mall", "Woolworths Queensgate", "Woolworths Lower Hutt","CentrePort Wellington"],
    ["CentrePort Wellington","Woolworths Aotea", "FreshChoice Cannons Creek", "Woolworths Tawa","CentrePort Wellington"]
]

demands = bootstrap_weekday_demand(weekday_demand_distribution)

route_demand_dict_working = {}
route_demand_dict_not_working = {}
route_names_working = []
total_demand_working = []
for route in routes:
    total_demand = 0
    for store in route:
        total_demand += demands[store]
    # make the route name a simple string (normal dict key)
    route_name = '->'.join(route)
    if total_demand <= 9:
        route_names_working.append(route_name)
        total_demand_working.append(total_demand)
        route_demand_dict_working[route_name] = total_demand
    else:
        route_demand_dict_not_working[route_name] = total_demand

print(route_demand_dict_working)



print(route_demand_dict_not_working)
print(route_names_working)
print(total_demand_working)










