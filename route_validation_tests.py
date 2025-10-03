# Testing Constraints
def close_enough(a, b, tol=1e-6):
    # Return True if a and b are within tolerance
    return abs(a - b) <= tol


def check_depot_starts_and_ends(routes, depot, sample_size=10):
    # Check that each sampled route starts and ends at the depot
    for route in routes[:sample_size]:
        starts_at_depot = (route[0] == depot)
        ends_at_depot = (route[-1] == depot)
        assert starts_at_depot and ends_at_depot, "Route does not start/end at " + depot + ": " + str(route)


def check_capacity(routes, demand_by_store, max_boxes, sample_size=10):
    # Check that total boxes on each sampled route stay within capacity
    for route in routes[:sample_size]:
        total_boxes = sum(demand_by_store.get(stop, 0) for stop in route)
        assert total_boxes <= max_boxes, "Route exceeds capacity (" + str(total_boxes) + " > " + str(
            max_boxes) + "): " + str(route)


def run_sample_route_check(lookup, demand_by_store):
    # Run a single sample route through time + cost and print a summary
    sample_route = ["Centre Port", "Woolworths Aotea", "Woolworths Karori", "Centre Port"]

    # Only run if all stops are in the demand dictionary
    if not all(stop in demand_by_store for stop in sample_route):
        print("Skipped sample route check (a stop is missing from the demand dictionary).")
        return

    travel_seconds = compute_travel_seconds(sample_route, lookup)
    unload_seconds = compute_unloading_seconds(sample_route, demand_by_store)

    total_minutes = (travel_seconds + unload_seconds) / 60.0
    base_m, ot_m, base_cost, ot_cost, total_cost = compute_costs(travel_seconds + unload_seconds)

    print("\n=== Sample Route Check ===")
    print("Route: " + "->".join(sample_route))
    print("Travel (min):  " + str(round(travel_seconds / 60.0, 1)))
    print("Unloading (min): " + str(round(unload_seconds / 60.0, 1)))
    print("Total (min):   " + str(round(total_minutes, 1)))
    print("Base (min):    " + str(round(base_m, 1)))
    print("Overtime (min): " + str(round(ot_m, 1)))
    print("Total cost ($): " + str(round(total_cost, 2)))

    # Base minutes + OT minutes should equal total minutes
    assert close_enough(base_m + ot_m, total_minutes), "Base + OT minutes should equal total minutes"

    
# Run tests
print("\nRunning simple tests...")
check_depot_starts_and_ends(tours_std, start, sample_size=10)
check_capacity(tours_std, demand_weekdays, max_demand_standard, sample_size=10)
run_sample_route_check(lookup, demand_weekdays)
print("All simple tests passed")





# Compare Ivy's duration vs Vishwas's
from duration_calculator import find_duration

def compare_ivy_and_vishwas(lookup, demand_by_store, duration_df):
    # Build index map directly from first column of CSV
    index_map = {name: i for i, name in enumerate(duration_df.iloc[:, 0])}

    # Define a sample route in both formats
    sample_route_list = ["Centre Port", "Woolworths Aotea", "Woolworths Karori", "Centre Port"]
    sample_route_str = "CentrePort Wellington->Woolworths Aotea->Woolworths Karori->CentrePort Wellington"

    # Vishwas calculation 
    travel_seconds = compute_travel_seconds(sample_route_list, lookup)
    unload_seconds = compute_unloading_seconds(sample_route_list, demand_by_store)
    vish_total_minutes = (travel_seconds + unload_seconds) / 60.0

    # Ivy calculation 
    tours = [sample_route_str]
    demand_total = [sum(demand_by_store.get(stop, 0) for stop in sample_route_list)]
    ivy_total_seconds = find_duration(tours, duration_df, index_map, demand_total)[0]
    ivy_total_minutes = ivy_total_seconds / 60.0

    # Print results side by side
    print("\n=== Ivy vs Vishwas Duration Check ===")
    print("Vishwas total (min): " + str(round(vish_total_minutes, 1)))
    print("Ivy total (min):     " + str(round(ivy_total_minutes, 1)))

    # Check they are close
    assert close_enough(vish_total_minutes, ivy_total_minutes), "Mismatch between Ivy and Vishwas durations!"
    print("✅ Ivy and Vishwas agree on route duration")

# Run comparison 
duration_df = pd.read_csv(matrix_csv)
compare_ivy_and_vishwas(lookup, demand_weekdays, duration_df)
