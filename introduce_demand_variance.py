import numpy
numpy.random.seed(42)

def generate_saturday_demand(stores, demand_limits):
    saturday_demand_dict = {}
    for store in stores:
        demand = numpy.random.uniform(low=0.0, high=demand_limits[store], size=None)
        if demand != 0:
            saturday_demand_dict[store] = demand

    return saturday_demand_dict

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
