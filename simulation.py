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
            duration[tour_number] += duration_data.iloc[prev_index, node_index + 1]
            prev = node
        duration[tour_number] += 15 * 60 * route_demand
        tour_number += 1
    return duration
