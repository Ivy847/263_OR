import numpy as np

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
    excess = total_demand - 9
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

if __name__ == '__main__':
    route = "CentrePort Wellington->Node1->Node2->Node3->Node4->CentrePort Wellington"
    requested_demands = {
        "CentrePort Wellington" : 0,
        "Node1" : 2,
        "Node2" : 5,
        "Node3" : 4,
        "Node4" : 3,
    }
    new_route, nodes_to_remove = handle_over_capacity_route(route, requested_demands)
    print(new_route)
    print(nodes_to_remove)