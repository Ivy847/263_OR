import numpy as np
import pandas as pd
import route_gen

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
    demand_weekdays = {
        "FreshChoice Cannons Creek": 3,
        "FreshChoice Cuba Street": 2,
        "FreshChoice Woburn": 2,
        "Metro Cable Car Lane": 2,
        "Woolworths Aotea": 3,
        "Woolworths Crofton Downs": 4,
        "Woolworths Johnsonville": 4,
        "Woolworths Johnsonville Mall": 3,
        "Woolworths Karori": 3,
        "Woolworths Kilbirnie": 3,
        "Woolworths Lower Hutt": 3,
        "Woolworths Maidstone": 4,
        "Woolworths Newtown": 3,
        "Woolworths Petone": 3,
        "Woolworths Porirua": 4,
        "Woolworths Queensgate": 3,
        "Woolworths Tawa": 2,
        "Woolworths Upper Hutt": 3,
        "Woolworths Wainuiomata": 4,
        "CentrePort Wellington": 0,
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
    start = "CentrePort Wellington"
    filename = "weekdayTours.txt"
    max_demand_per_route = 9

    weekday_standard_tours, demand_total = route_gen.generate_tours(nodes=nodes, demand=demand_weekdays, start=start,
                                            max_demand_per_route=max_demand_per_route, filename="weekdays_standard.txt")
    duration = find_duration(weekday_standard_tours, duration_dataset, index, demand_total)
    print(duration)
