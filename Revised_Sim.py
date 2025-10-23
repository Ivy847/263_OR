ORSkey = 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImEwMGM2OGNiZTE1NzQzZTBiM2MyY2U0NDdmZGVhMmU0IiwiaCI6Im11cm11cjY0In0='
import numpy as np
import pandas as pd

locations = pd.read_csv("WoolworthsLocations.csv")
import openrouteservice as ors

# Boot up client to OpenRouteService. ORSkey is your own key as a string.
client = ors.Client(key=ORSkey)
coords = locations[['Long', 'Lat']]  # Mapping packages work with Long, Lat arrays
coords = coords.to_numpy().tolist()  # Make the arrays into a list of lists.

# creates martrix of durations between points
matrix = client.distance_matrix(
    locations=coords,
    profile='driving-hgv',
    metrics=['duration'],
    validate=False,
)
names = locations["Store"].tolist()  # creates list of names
# Creates dataframe of durations with the store names
durations = pd.DataFrame(matrix['durations'], index=names, columns=names)

mean = 1.374
sigma = 0.116
low = 1
high = 2

sigma2 = np.log(1 + (sigma ** 2) / (mean ** 2))
sigma = np.sqrt(sigma2)
mu = np.log(mean) - 0.5 * sigma2
import numpy

numpy.random.seed(42)


def generate_saturday_demand(stores, demand_limits):
    d = {}
    for store in stores:
        hi = demand_limits[store]
        val = int(round(np.random.uniform(0.0, hi)))
        d[store] = val              # <-- keep zeroes too
    d["CentrePort Wellington"] = 0
    return d




def bootstrap_weekday_demand(store_demands):
    weekday_demand_dict = {}
    for store in store_demands:
        weekday_demand_dict[store] = numpy.random.choice(store_demands[store])

    return weekday_demand_dict


if __name__ == "__main__":
    store_names = {"FreshChoice Cannons Creek",
                   "FreshChoice Cuba Street",
                   "FreshChoice Woburn",
                   "Metro Cable Car Lane",
                   "Woolworths Aotea",
                   "Woolworths Crofton Downs",
                   "Woolworths Johnsonville",
                   "Woolworths Johnsonville Mall",
                   "Woolworths Karori",
                   "Woolworths Kilbirnie",
                   "Woolworths Lower Hutt",
                   "Woolworths Maidstone",
                   "Woolworths Newtown",
                   "Woolworths Petone",
                   "Woolworths Porirua",
                   "Woolworths Queensgate",
                   "Woolworths Tawa",
                   "Woolworths Upper Hutt",
                   "Woolworths Wainuiomata",
                   "CentrePort Wellington"}
    weekend_demand_limits = {
        "Woolworths Aotea": 1,
        "Woolworths Crofton Downs": 1,
        "Woolworths Johnsonville": 1,
        "Woolworths Johnsonville Mall": 1,
        "Woolworths Karori": 1,
        "Woolworths Kilbirnie": 1,
        "Woolworths Lower Hutt": 2,
        "Woolworths Newtown": 1,
        "Woolworths Petone": 1,
        "Woolworths Porirua": 1,
        "Woolworths Queensgate": 1,
        "Woolworths Tawa": 1,
        "Woolworths Upper Hutt": 1,
        "Woolworths Wainuiomata": 1,
        "CentrePort Wellington": 0,
    }
    weekday_demand_distribution = {
        "FreshChoice Cannons Creek": [3, 2, 2, 2, 1, 1, 1, 2, 1, 2, 3, 3, 3, 3, 4, 1, 1, 1, 2, 1],
        "FreshChoice Cuba Street": [1, 2, 2, 1, 2, 3, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 3, 2, 2],
        "FreshChoice Woburn": [2, 2, 3, 1, 1, 2, 2, 1, 1, 1, 3, 2, 3, 1, 2, 1, 2, 1, 1, 2],
        "Metro Cable Car Lane": [2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 5, 1, 2, 3, 2, 2, 1, 2, 2, 3],
        "Woolworths Aotea": [2, 5, 3, 2, 3, 2, 3, 2, 3, 2, 3, 3, 3, 2, 2, 1, 3, 1, 2, 1],
        "Woolworths Crofton Downs": [3, 2, 4, 2, 3, 1, 4, 4, 6, 2, 5, 2, 4, 3, 2, 1, 2, 2, 1, 2],
        "Woolworths Johnsonville": [3, 1, 2, 5, 3, 2, 5, 4, 3, 5, 5, 2, 1, 3, 3, 1, 2, 4, 3, 1],
        "Woolworths Johnsonville Mall": [2, 3, 4, 2, 3, 2, 3, 2, 1, 2, 1, 3, 1, 1, 4, 2, 1, 5, 1, 2],
        "Woolworths Karori": [2, 2, 3, 2, 3, 3, 2, 1, 2, 3, 3, 2, 4, 3, 3, 3, 2, 1, 2, 2],
        "Woolworths Kilbirnie": [2, 3, 4, 2, 2, 1, 2, 4, 3, 1, 2, 2, 2, 2, 3, 2, 3, 3, 3, 4],
        "Woolworths Lower Hutt": [2, 2, 1, 4, 1, 1, 2, 3, 2, 2, 3, 3, 5, 3, 1, 3, 3, 2, 2, 3],
        "Woolworths Maidstone": [3, 4, 2, 2, 2, 3, 5, 4, 3, 6, 2, 2, 2, 2, 1, 1, 1, 6, 3, 3],
        "Woolworths Newtown": [2, 4, 2, 5, 3, 3, 3, 5, 3, 2, 4, 1, 2, 3, 3, 1, 1, 3, 2, 3],
        "Woolworths Petone": [3, 5, 2, 2, 4, 1, 2, 2, 2, 3, 3, 3, 2, 2, 1, 2, 3, 2, 3, 2],
        "Woolworths Porirua": [5, 1, 5, 2, 2, 3, 2, 4, 1, 3, 3, 3, 3, 5, 2, 2, 2, 2, 4, 1],
        "Woolworths Queensgate": [2, 2, 3, 3, 4, 2, 2, 2, 2, 1, 2, 1, 4, 2, 2, 1, 2, 3, 1, 2, 4, 2, 2],
        "Woolworths Tawa": [2, 2, 2, 2, 2, 1, 1, 1, 1, 4, 2, 2, 1, 2, 3, 1, 2, 4, 2, 2],
        "Woolworths Upper Hutt": [2, 1, 2, 1, 1, 1, 2, 1, 1, 4, 3, 2, 4, 3, 2, 4, 1, 3, 2, 2],
        "Woolworths Wainuiomata": [3, 4, 2, 2, 2, 2, 2, 3, 3, 3, 1, 3, 2, 4, 2, 4, 5, 1, 1, 5],
        "CentrePort Wellington": [0],
    }


def get_cost(durations):
    costs = np.zeros(len(durations))
    i = 0
    for duration in durations:
        if duration > 3 * 60 * 60:
            overtime = duration - 3 * 60 * 60
            costs[i] += 3 * 60 * 60 * 0.055556
            costs[i] += overtime * 0.07639
        else:
            costs[i] += duration * 0.055556

        i += 1
    return costs


def get_costSub60(durations):
    """
    Charge $1000 for each started 4-hour block (4*3600 seconds).
    Example: 4h 00m 01s -> 2 blocks -> $2000
    """
    durations = np.asarray(durations, dtype=float)
    block_seconds = 4 * 60 * 60  # 14400
    blocks = np.ceil(durations / block_seconds)
    return 1000.0 * blocks


routes = [
    ["CentrePort Wellington", "Woolworths Porirua", "Woolworths Johnsonville", "CentrePort Wellington"],
    ["CentrePort Wellington", "Woolworths Upper Hutt", "Woolworths Maidstone", "CentrePort Wellington"],
    ["CentrePort Wellington", "Metro Cable Car Lane", "Woolworths Karori", "Woolworths Crofton Downs",
     "CentrePort Wellington"],
    ["CentrePort Wellington", "Woolworths Kilbirnie", "Woolworths Newtown", "FreshChoice Cuba Street",
     "CentrePort Wellington"],
    ["CentrePort Wellington", "Woolworths Petone", "Woolworths Wainuiomata", "FreshChoice Woburn",
     "CentrePort Wellington"],
    ["CentrePort Wellington", "Woolworths Johnsonville Mall", "Woolworths Queensgate", "Woolworths Lower Hutt",
     "CentrePort Wellington"],
    ["CentrePort Wellington", "Woolworths Aotea", "FreshChoice Cannons Creek", "Woolworths Tawa",
     "CentrePort Wellington"]
]

routes_saturday = [
    ["CentrePort Wellington", "Woolworths Kilbirnie", "Woolworths Newtown", "CentrePort Wellington"],
    ["CentrePort Wellington", "Woolworths Petone", "Woolworths Wainuiomata", "Woolworths Queensgate",
     "Woolworths Lower Hutt", "CentrePort Wellington"],
    ["CentrePort Wellington", "Woolworths Upper Hutt", "Woolworths Aotea", "Woolworths Porirua", "Woolworths Tawa",
     "CentrePort Wellington"],
    ["CentrePort Wellington", "Woolworths Karori", "Woolworths Crofton Downs", "Woolworths Johnsonville Mall",
     "Woolworths Johnsonville", "CentrePort Wellington"]
]
import numpy as np
import pandas as pd


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
    "Woolworths Aotea": 0,
    "Woolworths Crofton Downs": 1,
    "Woolworths Johnsonville": 2,
    "Woolworths Johnsonville Mall": 3,
    "Woolworths Karori": 4,
    "Woolworths Kilbirnie": 5,
    "Woolworths Lower Hutt": 6,
    "Woolworths Maidstone": 7,
    "Woolworths Newtown": 8,
    "Woolworths Petone": 9,
    "Woolworths Porirua": 10,
    "Woolworths Queensgate": 11,
    "Woolworths Tawa": 12,
    "Woolworths Upper Hutt": 13,
    "Woolworths Wainuiomata": 14,
    "FreshChoice Cuba Street": 15,
    "FreshChoice Woburn": 16,
    "FreshChoice Cannons Creek": 17,
    "Metro Cable Car Lane": 18,
    "CentrePort Wellington": 19,
}


def handle_over_capacity_routesub60(route, requested_demands):
    '''
    Parameters
    ----------
    route: str containing route in the format: "node1->node2->node3"
    requested_demands: dict with node names as keys, and node demands as values

    Returns
    --------
    new_route: str containing new route in the format: "node1->node2->node3"
    nodes_to_remove: dict with nodes names removed from the route as keys, and node demands as values
    '''
    nodes = route.split('->')
    total_demand = sum(requested_demands.values())
    excess = total_demand - 4
    nodes_to_remove = {}
    i = 0

    while sum(nodes_to_remove.values()) < excess:
        nodes_to_remove[nodes[i]] = requested_demands[nodes[i]]
        i += 1

    new_route = "CentrePort Wellington->"
    for node in nodes:
        if node in nodes_to_remove:
            continue
        else:
            new_route += node
            new_route += "->"
    new_route += "CentrePort Wellington"

    return new_route, nodes_to_remove


def handle_over_capacity_route(route, requested_demands):
    '''
    Parameters
    ----------
    route: str containing route in the format: "node1->node2->node3"
    requested_demands: dict with node names as keys, and node demands as values

    Returns
    --------
    new_route: str containing new route in the format: "node1->node2->node3"
    nodes_to_remove: dict with nodes names removed from the route as keys, and node demands as values
    '''
    nodes = route.split('->')
    total_demand = sum(requested_demands.values())
    capacity_limit = 9
    nodes_to_remove = {}

    # Create a list of (node, demand) tuples
    node_demand_list = [(node, requested_demands[node]) for node in nodes]
    # Sort by demand ascending
    node_demand_list_sorted = sorted(node_demand_list, key=lambda x: x[1])

    demand_sum = total_demand

    # Remove nodes with the lowest demand until under capacity
    for node, demand in node_demand_list_sorted:
        if demand_sum <= capacity_limit:
            break
        nodes_to_remove[node] = demand
        demand_sum -= demand

    # Rebuild route excluding removed nodes, maintaining original order
    new_nodes = [node for node in nodes if node not in nodes_to_remove]
    new_route = "CentrePort Wellington->" + "->".join(new_nodes) + "->CentrePort Wellington"

    return new_route, nodes_to_remove


def WW_routes_over(route_names_not_working, demands, route_names_working, total_demand_working):
    # input: a list of str containing route in the format: "node1->node2->node3" so a list of the routes which go over capcity
    # demands is the list of demands for each store/

    extra_route_nodes = []
    extra_route_demand = 0
    # runs through each route which is over capacity
    for route in range(len(route_names_not_working)):
        routes_demands = {}
        total_demand = 0

        # gets the nodes of the route which isnt working
        nodes = route_names_not_working[route].split('->')

        # runs though the list of nodes in that route
        for node in nodes:
            # creates a dictionary of the nodes in that route.
            routes_demands[node] = demands[node]

        # creates new route and gives back the nodes to remove.
        new_route, nodes_to_remove = handle_over_capacity_route(route_names_not_working[route], routes_demands)

        # need to find the total demand for that route:
        New_route_nodes = new_route.split('->')
        for node in New_route_nodes:
            total_demand += demands[node]

        # add working route to the lists.
        route_names_working.append(new_route)
        total_demand_working.append(total_demand)

        # now what to do with the rest of the nodes:
        for key in list(nodes_to_remove.keys())[1:]:
            extra_route_nodes.append(key)
        extra_route_demand += sum(nodes_to_remove.values())

    return extra_route_nodes, extra_route_demand


total_costs = []
count_no_change = 0
count_extra_route = 0
routes_sub60s = 0
for i in range(10000):
    rng = np.random.default_rng()  # sets random seed

    multiplier_matrix = rng.lognormal(mean=mu, sigma=sigma,
                                      size=durations.shape)  # creates a matrix with random mulitplers
    multiplier_matrix = np.clip(multiplier_matrix, low, high)  # makes sure no values go over or under the max and min

    var_durations = pd.DataFrame(durations.to_numpy() * multiplier_matrix, index=durations.index,
                                 columns=durations.columns)
    demands = bootstrap_weekday_demand(weekday_demand_distribution)

    route_demand_dict_working = {}
    route_demand_dict_not_working = {}
    route_names_working = []
    total_demand_working = []
    route_names_not_working = []
    route_namessub60 = []
    total_demand_sub60 = []

    # this appends working routes and there demand to the total demand working and the routes names
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
            count_no_change += 1
        else:
            route_demand_dict_not_working[route_name] = total_demand
            route_names_not_working.append(route_name)
            count_extra_route += 1

        # gives a list of the routes which are not working and a dictionary of the route name and its total demand.

    # dont know what to do with the nodes to remove yet lol spare_stores = {}

    if route_names_not_working:

        # this changes the routes which dont work and add them to the working list and passes back the extra nodes which were taken out of the route
        # and gives the total demand of the route.
        extra_route_nodes, extra_route_demand = WW_routes_over(route_names_not_working, demands, route_names_working,
                                                               total_demand_working)

        # now i need to create a new route with the nodes I have left. so we have one ww route left.
        # so if the rest of the nodes combined is less than or equal to 9 i can just make one more woolworths route.
        new_route_name = 'CentrePort Wellington->' + '->'.join(extra_route_nodes) + '->CentrePort Wellington'
        if extra_route_demand <= 9:

            route_names_working.append(new_route_name)
            total_demand_working.append(extra_route_demand)
        # if the routes demand is over 9 then use the function to get a route and the extra nodes.
        else:
            # create a dictionary of the nodes and their demands.
            routes_demands = {}
            nodes = new_route_name.split('->')
            # runs through the list of nodes in that route
            for node in nodes:
                # creates a dictionary of the nodes in that route.
                routes_demands[node] = demands[node]

            # returns a working route and the nodes to remove
            new_route, nodes_to_remove = handle_over_capacity_route(new_route_name, routes_demands)
            # ok so some of the nodes to remove are larger than 4 so cant go on the sub60 routes.

            # find the demand dictionary of the new route:
            New_route_nodes = new_route.split('->')
            total_demand = 0
            for node in New_route_nodes:
                total_demand += demands[node]
            route_names_working.append(new_route)
            total_demand_working.append(total_demand)
            # ok need to create something which uses the sub60 vans:

            if nodes_to_remove:
                total_demand_to_remove = sum(nodes_to_remove.values())
                if total_demand_to_remove <= 4:
                    sub_new_route_name = '->'.join(nodes_to_remove.keys()) + '->CentrePort Wellington'

                    route_namessub60.append(sub_new_route_name)
                    total_demand_sub60.append(total_demand_to_remove)
                    routes_sub60s += 1
                else:
                    last_node_key, last_node_value = nodes_to_remove.popitem()

                    routeone_name = '->'.join(nodes_to_remove.keys()) + '->CentrePort Wellington'
                    routetwo_name = 'CentrePort Wellington->' + last_node_key + '->CentrePort Wellington'

                    route_namessub60.append(routeone_name)
                    total_demand_sub60.append(sum(nodes_to_remove.values()))

                    route_namessub60.append(routetwo_name)
                    total_demand_sub60.append(last_node_value)
                    routes_sub60s += 1

    # now i need to figure out what to do with the sub 60 vans and how to make there routes

    durations_new = find_duration_simulation(route_names_working, var_durations, index, total_demand_working)
    costs = get_cost(durations_new)

    durationssub60 = find_duration_simulation(route_namessub60, var_durations, index, total_demand_sub60)
    costssub60 = get_costSub60(durationssub60)

    total_cost = np.sum(costs) + np.sum(costssub60)
    total_costs.append(total_cost)
print(routes_sub60s)
import matplotlib.pyplot as plt

# plot total costs over simulations
plt.figure(figsize=(8, 5))
plt.plot(total_costs)
plt.title("Total Route Costs per Simulation")
plt.xlabel("Simulation run")
plt.ylabel("Total cost ($)")
plt.show()
import matplotlib.pyplot as plt
import numpy as np

# Convert to numpy array for easier calculations
total_costs_array = np.array(total_costs)

# Calculate percentiles for confidence interval
alpha = 0.05  # 95% confidence interval
lower_percentile = 100 * (alpha / 2)
upper_percentile = 100 * (1 - alpha / 2)

lower_bound = np.percentile(total_costs_array, lower_percentile)
upper_bound = np.percentile(total_costs_array, upper_percentile)
mean_cost = np.mean(total_costs_array)
median_cost = np.median(total_costs_array)

# Create graphs
plt.figure(figsize=(15, 5))

# Plot 1: Histogram of total costs with confidence interval
plt.subplot(1, 2, 1)
n, bins, patches = plt.hist(total_costs_array, bins=30, edgecolor='black', alpha=0.7)
plt.axvline(lower_bound, color='red', linestyle='--', linewidth=2, label=f'95% CI Lower: ${lower_bound:.2f}')
plt.axvline(upper_bound, color='red', linestyle='--', linewidth=2, label=f'95% CI Upper: ${upper_bound:.2f}')
plt.axvline(mean_cost, color='green', linestyle='-', linewidth=2, label=f'Mean: ${mean_cost:.2f}')
plt.axvline(median_cost, color='orange', linestyle='-', linewidth=2, label=f'Median: ${median_cost:.2f}')
plt.title('Distribution of Total Costs with 95% Confidence Interval')
plt.xlabel('Total Cost ($)')
plt.ylabel('Count')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Box plot
plt.subplot(1, 2, 2)
plt.boxplot(total_costs_array)
plt.title('Box Plot of Total Costs')
plt.ylabel('Total Cost ($)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print detailed statistics and answers
print("=" * 60)
print("SIMULATION RESULTS ANALYSIS")
print("=" * 60)

print(f"\nBASIC STATISTICS:")
print(f"Number of simulations: {len(total_costs_array)}")
print(f"Mean total cost: ${mean_cost:.2f}")
print(f"Median total cost: ${median_cost:.2f}")
print(f"Standard deviation: ${np.std(total_costs_array):.2f}")
print(f"Minimum cost: ${np.min(total_costs_array):.2f}")
print(f"Maximum cost: ${np.max(total_costs_array):.2f}")

print(f"\n95% CONFIDENCE INTERVAL RESULTS:")
print(f"Lower bound (2.5th percentile): ${lower_bound:.2f}")
print(f"Upper bound (97.5th percentile): ${upper_bound:.2f}")
print(f"Confidence interval range: ${upper_bound - lower_bound:.2f}")

print(f"\nINTERPRETATION:")
print(f"Based on {len(total_costs_array)} simulations, we are 95% confident that")
print(f"the true total cost of the delivery routes falls between ${lower_bound:.2f}")
print(f"and ${upper_bound:.2f}. The average expected cost is approximately ${mean_cost:.2f}.")

print(f"\nKEY PERCENTILES:")
percentiles = [2.5, 5, 25, 50, 75, 95, 97.5]
for p in percentiles:
    value = np.percentile(total_costs_array, p)
    print(f"  {p}th percentile: ${value:.2f}")

print(f"\nCOST RANGE ANALYSIS:")
print(
    f"Middle 50% of costs range from ${np.percentile(total_costs_array, 25):.2f} to ${np.percentile(total_costs_array, 75):.2f}")
print(f"90% of costs are below: ${np.percentile(total_costs_array, 90):.2f}")
print(f"Only 5% of costs exceed: ${np.percentile(total_costs_array, 95):.2f}")

import matplotlib.pyplot as plt


def saturday_simulation():
    total_costs = []
    count_no_change = 0
    count_extra_route = 0

    for i in range(1000):
        rng = np.random.default_rng()

        multiplier_matrix = rng.lognormal(mean=mu, sigma=sigma, size=durations.shape)
        multiplier_matrix = np.clip(multiplier_matrix, low, high)

        var_durations = pd.DataFrame(durations.to_numpy() * multiplier_matrix, index=durations.index,
                                     columns=durations.columns)

        # Get only the stores that appear in Saturday routes
        stores_in_saturday_routes = {store for route in routes_saturday for store in route}

        # Generate Saturday demands only for stores in Saturday routes
        demands = generate_saturday_demand(stores_in_saturday_routes, weekend_demand_limits)

        # Add CentrePort Wellington with 0 demand to avoid KeyError
        demands["CentrePort Wellington"] = 0

        route_names_working = []
        total_demand_working = []
        route_names_not_working = []

        # Use Saturday routes
        for route in routes_saturday:
            total_demand = 0
            for store in route:
                total_demand += demands[store]

            route_name = '->'.join(route)
            if total_demand <= 9:
                route_names_working.append(route_name)
                total_demand_working.append(total_demand)
                count_no_change += 1
            else:
                route_names_not_working.append(route_name)
                count_extra_route += 1

        # Handle over-capacity routes
        if route_names_not_working:
            extra_route_nodes, extra_route_demand = WW_routes_over(route_names_not_working, demands,
                                                                   route_names_working, total_demand_working)

            new_route_name = 'CentrePort Wellington->' + '->'.join(extra_route_nodes) + '->CentrePort Wellington'
            if extra_route_demand <= 9:
                route_names_working.append(new_route_name)
                total_demand_working.append(extra_route_demand)
            else:
                routes_demands = {}
                nodes = new_route_name.split('->')
                for node in nodes:
                    routes_demands[node] = demands[node]

                new_route, nodes_to_remove = handle_over_capacity_route(new_route_name, routes_demands)

                New_route_nodes = new_route.split('->')
                total_demand = 0
                for node in New_route_nodes:
                    total_demand += demands[node]
                route_names_working.append(new_route)
                total_demand_working.append(total_demand)

        # Calculate costs
        durations_new = find_duration_simulation(route_names_working, var_durations, index, total_demand_working)
        costs = get_cost(durations_new)

        total_cost = np.sum(costs)
        total_costs.append(total_cost)

    return total_costs, count_no_change, count_extra_route


# Run Saturday simulation
saturday_costs, sat_count_no_change, sat_count_extra_route = saturday_simulation()

# Analyze Saturday results
saturday_costs_array = np.array(saturday_costs)

# Calculate statistics
sat_mean = np.mean(saturday_costs_array)
sat_median = np.median(saturday_costs_array)
sat_std = np.std(saturday_costs_array)
sat_lower_ci = np.percentile(saturday_costs_array, 2.5)
sat_upper_ci = np.percentile(saturday_costs_array, 97.5)

print("SATURDAY SIMULATION RESULTS")
print("=" * 50)
print(f"Mean cost: ${sat_mean:.2f}")
print(f"Median cost: ${sat_median:.2f}")
print(f"95% CI: ${sat_lower_ci:.2f} - ${sat_upper_ci:.2f}")
print(f"Standard deviation: ${sat_std:.2f}")
print(f"Routes unchanged: {sat_count_no_change}")
print(f"Routes needing adjustment: {sat_count_extra_route}")

# Plot Saturday results
plt.figure(figsize=(15, 5))

# Plot 1: Histogram
plt.subplot(1, 2, 1)
n, bins, patches = plt.hist(saturday_costs_array, bins=30, edgecolor='black', alpha=0.7)
plt.axvline(sat_lower_ci, color='red', linestyle='--', linewidth=2, label=f'95% CI Lower: ${sat_lower_ci:.2f}')
plt.axvline(sat_upper_ci, color='red', linestyle='--', linewidth=2, label=f'95% CI Upper: ${sat_upper_ci:.2f}')
plt.axvline(sat_mean, color='green', linestyle='-', linewidth=2, label=f'Mean: ${sat_mean:.2f}')
plt.title('Saturday: Distribution of Total Costs')
plt.xlabel('Total Cost ($)')
plt.ylabel('Count')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Route outcomes
plt.subplot(1, 2, 2)
labels = ["WW unchanged (≤9)", "WW over-capacity (>9)"]
values = [sat_count_no_change, sat_count_extra_route]
plt.bar(labels, values, color=['#4CAF50', '#FF9800'])
plt.title('Saturday: Route Outcomes')
plt.ylabel('Count')
plt.xticks(rotation=10)

plt.tight_layout()
plt.show()









# Reduced Fleet Simulation: WW vs Sub60 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants for Sub60 pricing
RF_SUB60_BLOCK_SEC  = 4 * 60 * 60      # 4 hours in seconds
RF_SUB60_BLOCK_COST = 1000.0
RF_SUB60_VAN_CAP    = 4                # boxes per Sub60 van

def rf_route_costs_ww_vs_sub60(route_name, var_durations, index_map, route_demand):
    """
    Returns: (ww_cost, sub60_cost, benefit=sub60_cost - ww_cost)
    - WW cost: piecewise rate with overtime; infinite if route_demand > 9 (not WW-eligible)
    - Sub60 cost: vans_needed * blocks * $1000
    """
    dur = find_duration_simulation([route_name], var_durations, index_map, [route_demand])[0]
    # WW cost: only if eligible (<= 9 boxes)
    ww_cost = get_cost([dur])[0] if route_demand <= 9 else np.inf
    # Sub60 cost: vans * time blocks
    vans_needed = int(np.ceil(route_demand / RF_SUB60_VAN_CAP)) if route_demand > 0 else 0
    blocks = int(np.ceil(dur / RF_SUB60_BLOCK_SEC)) if dur > 0 else 0
    sub60_cost = RF_SUB60_BLOCK_COST * vans_needed * blocks
    return ww_cost, sub60_cost, (sub60_cost - ww_cost)

def rf_saturday_simulate_fleet(F, n_runs=2000, include_fixed=False, fixed_per_van_per_year=50000, days_per_year=312):
    """
    Saturday reduced-fleet simulation:
      - At most 2F WW routes/day
      - Choose the WW-eligible routes (<=9 boxes) with largest (Sub60 - WW) benefit
      - Others go to Sub60
      - Optional fixed fleet cost per van/day
    Returns: np.array of total daily costs (length n_runs)
    """
    rng = np.random.default_rng(12345 + F)
    fixed_daily = (fixed_per_van_per_year * F) / days_per_year if include_fixed else 0.0
    stores_in_sat = {s for r in routes_saturday for s in r}
    totals = []

    for _ in range(n_runs):
        # Traffic draw & clip
        mult = rng.lognormal(mean=mu, sigma=sigma, size=durations.shape)
        mult = np.clip(mult, low, high)
        var_durs = pd.DataFrame(durations.to_numpy() * mult, index=durations.index, columns=durations.columns)

        # Demand draw (integer boxes)
        demands = generate_saturday_demand(stores_in_sat, weekend_demand_limits)

        # Per-route demand/costs
        rnames = ['->'.join(r) for r in routes_saturday]
        rdem   = [sum(demands.get(s, 0) for s in r) for r in routes_saturday]

        ww_costs, sub_costs, benefits, eligible = [], [], [], []
        for rn, rd in zip(rnames, rdem):
            cww, csub, ben = rf_route_costs_ww_vs_sub60(rn, var_durs, index, rd)
            ww_costs.append(cww); sub_costs.append(csub); benefits.append(ben)
            eligible.append(np.isfinite(cww))  # eligible if ≤9 boxes

        # Pick top-K WW routes (K = 2F)
        K = min(2*F, len(rnames))
        eligible_idx = [i for i, ok in enumerate(eligible) if ok]
        order = sorted(eligible_idx, key=lambda i: benefits[i], reverse=True)
        keep = set(order[:K])

        # Total cost for the day
        total = fixed_daily
        for i in range(len(rnames)):
            total += ww_costs[i] if i in keep else sub_costs[i]
        totals.append(total)

    return np.array(totals)

def rf_weekday_simulate_fleet(F, n_runs=2000, include_fixed=True, fixed_per_van_per_year=50000, days_per_year=312):
    """
    Weekday reduced-fleet simulation:
      - At most 2F WW routes/day among the 7 weekday routes
      - Choose top (Sub60 - WW) benefit routes to keep WW; rest to Sub60
      - Include optional fixed fleet cost
    """
    rng = np.random.default_rng(54321 + F)
    fixed_daily = (fixed_per_van_per_year * F) / days_per_year if include_fixed else 0.0
    totals = []

    for _ in range(n_runs):
        # Traffic draw & clip
        mult = rng.lognormal(mean=mu, sigma=sigma, size=durations.shape)
        mult = np.clip(mult, low, high)
        var_durs = pd.DataFrame(durations.to_numpy() * mult, index=durations.index, columns=durations.columns)

        # Demand draw
        demands = bootstrap_weekday_demand(weekday_demand_distribution)

        # Per-route demand/costs
        rnames = ['->'.join(r) for r in routes]
        rdem   = [sum(demands.get(s, 0) for s in r) for r in routes]

        ww_costs, sub_costs, benefits, eligible = [], [], [], []
        for rn, rd in zip(rnames, rdem):
            cww, csub, ben = rf_route_costs_ww_vs_sub60(rn, var_durs, index, rd)
            ww_costs.append(cww); sub_costs.append(csub); benefits.append(ben)
            eligible.append(np.isfinite(cww))  # ≤9 boxes

        # Pick top-K WW routes (K = 2F)
        K = min(2*F, len(rnames))
        eligible_idx = [i for i, ok in enumerate(eligible) if ok]
        order = sorted(eligible_idx, key=lambda i: benefits[i], reverse=True)
        keep = set(order[:K])

        # Total cost
        total = fixed_daily
        for i in range(len(rnames)):
            total += ww_costs[i] if i in keep else sub_costs[i]
        totals.append(total)

    return np.array(totals)

# helper function for 95% bootstrap CI of the mean
def rf_bootstrap_mean_ci(arr, B=3000, alpha=0.05, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    arr = np.asarray(arr)
    n = arr.size
    boots = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n)
        boots[b] = arr[idx].mean()
    lo = np.percentile(boots, 100*(alpha/2))
    hi = np.percentile(boots, 100*(1 - alpha/2))
    return arr.mean(), lo, hi


# Saturday 2 vs 3 vans (operating cost only - No Fixed cost)
rf_sat2 = rf_saturday_simulate_fleet(F=2, n_runs=2000, include_fixed=False)
rf_sat3 = rf_saturday_simulate_fleet(F=3, n_runs=2000, include_fixed=False)

print("\nSaturday mean costs (no fixed):")
print("  2 vans:", rf_sat2.mean(), " 95% CI:", np.percentile(rf_sat2,[2.5,97.5]))
print("  3 vans:", rf_sat3.mean(), " 95% CI:", np.percentile(rf_sat3,[2.5,97.5]))

plt.figure(figsize=(7,4))
plt.boxplot([rf_sat2, rf_sat3], labels=["2 vans","3 vans"], showmeans=True)
plt.ylabel("Total daily cost ($)")
plt.title("Saturday: Cost Distribution (2 vs 3 WW vans)")
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

sat_labels = ["2 vans", "3 vans"]
sat_means_lo_hi = [rf_bootstrap_mean_ci(rf_sat2), rf_bootstrap_mean_ci(rf_sat3)]
sat_means  = [m for (m, lo, hi) in sat_means_lo_hi]
sat_err_lo = [m - lo for (m, lo, hi) in sat_means_lo_hi]
sat_err_hi = [hi - m for (m, lo, hi) in sat_means_lo_hi]
sat_yerr   = [sat_err_lo, sat_err_hi]

x = np.arange(len(sat_labels))
plt.figure(figsize=(7, 4.5))
plt.errorbar(x, sat_means, yerr=sat_yerr, fmt='-o', capsize=5)
plt.xticks(x, sat_labels)
plt.ylabel("Mean total daily cost ($)")
plt.title("Saturday: Cost vs Fleet Size (2 vs 3 WW vans) — 95% CI")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Histograms for Saturday (2 vs 3 vans)
plt.figure(figsize=(8, 5))
sat_min = min(rf_sat2.min(), rf_sat3.min())
sat_max = max(rf_sat2.max(), rf_sat3.max())
sat_bins = np.linspace(sat_min, sat_max, 40)

plt.hist(rf_sat2, bins=sat_bins, alpha=0.6, edgecolor='black', label='2 vans')
plt.hist(rf_sat3, bins=sat_bins, alpha=0.6, edgecolor='black', label='3 vans')

plt.axvline(rf_sat2.mean(), linestyle='--', linewidth=2, label=f'2 vans mean: ${rf_sat2.mean():.0f}')
plt.axvline(rf_sat3.mean(), linestyle='--', linewidth=2, label=f'3 vans mean: ${rf_sat3.mean():.0f}')

plt.title('Saturday: Total Daily Cost Distribution (with fixed)')
plt.xlabel('Total daily cost ($)')
plt.ylabel('Count')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# Weekday 3 vs 4 vans (fixed included)
rf_wk3 = rf_weekday_simulate_fleet(F=3, n_runs=2000, include_fixed=True)
rf_wk4 = rf_weekday_simulate_fleet(F=4, n_runs=2000, include_fixed=True)

m3, lo3, hi3 = rf_bootstrap_mean_ci(rf_wk3)
m4, lo4, hi4 = rf_bootstrap_mean_ci(rf_wk4)
print("\nWEEKDAY mean costs (fixed included):")
print(f"  3 vans: ${m3:,.0f}   95% CI for mean: (${lo3:,.0f}, ${hi3:,.0f})")
print(f"  4 vans: ${m4:,.0f}   95% CI for mean: (${lo4:,.0f}, ${hi4:,.0f})")

wk_labels = ["3 vans", "4 vans"]
wk_means  = [m3, m4]
wk_yerr   = [[m3 - lo3, m4 - lo4], [hi3 - m3, hi4 - m4]]

x = np.arange(len(wk_labels))
plt.figure(figsize=(7, 4.5))
plt.errorbar(x, wk_means, yerr=wk_yerr, fmt='-o', capsize=5)
plt.xticks(x, wk_labels)
plt.ylabel("Mean total daily cost ($)")
plt.title("Weekday: Cost vs Fleet Size (3 vs 4 WW vans) — 95% CI")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

plt.figure(figsize=(7, 4.5))
plt.boxplot([rf_wk3, rf_wk4], labels=wk_labels, showmeans=True)
plt.ylabel("Total daily cost ($)")
plt.title("Weekday: Cost Distribution (3 vs 4 WW vans)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- HISTOGRAMS: Weekday (3 vs 4 vans) ---
plt.figure(figsize=(8, 5))
wk_min = min(rf_wk3.min(), rf_wk4.min())
wk_max = max(rf_wk3.max(), rf_wk4.max())
wk_bins = np.linspace(wk_min, wk_max, 40)

plt.hist(rf_wk3, bins=wk_bins, alpha=0.6, edgecolor='black', label='3 vans')
plt.hist(rf_wk4, bins=wk_bins, alpha=0.6, edgecolor='black', label='4 vans')

plt.axvline(rf_wk3.mean(), linestyle='--', linewidth=2, label=f'3 vans mean: ${rf_wk3.mean():.0f}')
plt.axvline(rf_wk4.mean(), linestyle='--', linewidth=2, label=f'4 vans mean: ${rf_wk4.mean():.0f}')

plt.title('Weekday: Total Daily Cost Distribution (with fixed)')
plt.xlabel('Total daily cost ($)')
plt.ylabel('Count')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
