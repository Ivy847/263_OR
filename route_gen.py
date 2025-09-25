import itertools

def generate_tours(nodes, start, filename="tours.txt"):
    """
    Generate all tours starting and ending at 'start',
    visiting up to 4 distinct intermediate nodes.

    Args:
        nodes (set): Set of distinct nodes (including start).
        start: The starting node.
        filename (str): File to save tours into.
    """
    # Ensure start is in the nodes set
    if start not in nodes:
        raise ValueError("Starting node must be in the set of nodes.")

    tours = []
    other_nodes = nodes - {start}

    # Generate tours with 1 to 4 intermediate nodes
    for r in range(1, 5):
        # generates all possible ordered arrangements (of length r, using nodes that are not the start node)
        for perm in itertools.permutations(other_nodes, r):
            # record all the possible paths of this length
            path = [start] + list(perm) + [start]
            tours.append("->".join(path))

    # Write tours to file
    with open(filename, "w") as f:
        for tour in tours:
            f.write(tour + "\n")

    print(f"Saved {len(tours)} tours to {filename}")

if __name__ == '__main__':
    nodes = {"FreshChoice Cannons Creek",
             "FreshChoice Cuba Street"
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
             "Centre Port"}
    start = "Centre Port"
    generate_tours(nodes, start, filename="tours.txt")
