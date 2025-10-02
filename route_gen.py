import itertools
import pandas as pd
import numpy as np
from pandas import read_csv


def generate_tours(nodes, demand, start, max_demand_per_route, filename):
    """
    Generate all tours starting and ending at 'start',
    visiting up to 4 distinct intermediate nodes.

    Args:
        nodes (set): Set of distinct nodes (including start).
        demand: dictionary mapping the expected demand to the relevant store.
        start: The starting node.
        max_demand_per_route (int): The maximum demand per route.
        filename (str): File to save tours into.
    """
    # Ensure start is in the nodes set
    if start not in nodes:
        raise ValueError("Starting node must be in the set of nodes.")

    tours = []
    other_nodes = nodes - {start}
    demand_total = []

    # Generate tours with 1 to 4 intermediate nodes
    for r in range(1, 5):
        # generates all possible ordered arrangements (of length r, using nodes that are not the start node)
        for perm in itertools.permutations(other_nodes, r):
            # record all the possible paths of this length
            path = [start] + list(perm) + [start]
            # check that the path is valid with demand
            total = 0
            for store in path:
                total += demand[store]
            if total <= max_demand_per_route:
                tours.append("->".join(path))
                demand_total.append(total)

    # Write tours to file
    with open(filename, "w") as f:
        for tour in tours:
            f.write(tour + "\n")

    print(f"Saved {len(tours)} tours to {filename}")
    return tours, demand_total

def find_duration(tours, duration_data, index, demand_total):
    duration = np.zeros(len(tours))
    tour_number = 0
    for tour in tours:
        nodes = tour.split('->')
        route_demand = demand_total[tour_number]
        prev = "CentrePort Wellington"
        for node in nodes:
            prev_index = index[prev]
            node_index = index[node]
            duration[tour_number] += duration_data.iloc[prev_index, node_index+1]
            prev = node
        duration[tour_number] += 15 * 60 * route_demand
        tour_number += 1
    return duration

if __name__ == '__main__':
    duration_dataset = pd.read_csv("WoolworthsDurations2025.csv")
    print(duration_dataset.index)
    nodes = {"FreshChoice Cannons Creek",
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
    start = "CentrePort Wellington"
    demand_weekdays = {
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
    demand_saturdays = {
        "FreshChoice Cannons Creek": 0,
        "FreshChoice Cuba Street": 0,
        "FreshChoice Woburn": 0,
        "Metro Cable Car Lane": 0,
        "Woolworths Aotea": 0,
        "Woolworths Crofton Downs": 0,
        "Woolworths Johnsonville": 0,
        "Woolworths Johnsonville Mall": 0,
        "Woolworths Karori": 0,
        "Woolworths Kilbirnie": 0,
        "Woolworths Lower Hutt": 0,
        "Woolworths Maidstone": 0,
        "Woolworths Newtown": 0,
        "Woolworths Petone": 0,
        "Woolworths Porirua": 0,
        "Woolworths Queensgate": 0,
        "Woolworths Tawa": 0,
        "Woolworths Upper Hutt": 0,
        "Woolworths Wainuiomata": 0,
        "CentrePort Wellington": 0,
    }
    filename = "weekdayTours.txt"
    max_demand_per_route = 9
    max_demand_per_route_extra = 4
    weekday_standard_tours = generate_tours(nodes=nodes, demand=demand_weekdays, start=start, max_demand_per_route=max_demand_per_route, filename="weekdays_standard.txt")
    weekday_extra_tours = generate_tours(nodes=nodes, demand=demand_weekdays, start=start, max_demand_per_route=max_demand_per_route_extra,
                   filename="weekdays_extra.txt")
    #generate_tours(nodes=nodes, demand=demand_saturdays, start=start, max_demand_per_route=max_demand_per_route,
    #               filename=filename)
    #generate_tours(nodes=nodes, demand=demand_saturdays, start=start, max_demand_per_route=max_demand_per_route,
    #               filename=filename)

