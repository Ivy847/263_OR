import itertools
from pathlib import Path
import pandas as pd

# Line up depot name with the matrix
NAME_MAP = {"Centre Port": "CentrePort Wellington"}


def norm(name: str) -> str:
    return NAME_MAP.get(name.strip(), name.strip())


def build_lookup(matrix_csv: Path):
    df = pd.read_csv(matrix_csv)
    df = df.rename(columns={df.columns[0]: "origin"})
    dests = [c for c in df.columns if c != "origin"]
    lookup = {}
    for _, row in df.iterrows():
        o = str(row["origin"]).strip()
        for d in dests:
            val = row[d]
            if pd.notnull(val):
                lookup[(o, d)] = float(val)  # seconds from matrix
    return lookup


def generate_tours(nodes, demand, start, max_demand, max_intermediate=4):
    others = list(nodes - {start})
    tours = []
    for r in range(1, max_intermediate + 1):
        for perm in itertools.permutations(others, r):
            path = [start] + list(perm) + [start]
            if sum(demand[s] for s in path) <= max_demand:
                tours.append(path)
    return tours


def compute_travel_seconds(stops, lookup):
    total = 0.0
    for a, b in zip(stops[:-1], stops[1:]):
        t = lookup.get((norm(a), norm(b)))
        if t is None:
            return None
        total += t
    return total


def compute_unloading_seconds(
    stops, demand, depot_name="Centre Port", unload_minutes_per_box=15
):
    unload_sec_per_box = unload_minutes_per_box * 60.0
    intermediates = stops[1:-1]
    total_unload = 0.0
    for store in intermediates:
        boxes = demand.get(store, 0)
        total_unload += boxes * unload_sec_per_box
    return total_unload


# with the Cost parameters
SHIFT_MINUTES = 180.0
BASE_RATE_PER_HR = 200.0
OT_RATE_PER_HR = 275.0
BASE_RATE_PER_MIN = BASE_RATE_PER_HR / 60.0
OT_RATE_PER_MIN = OT_RATE_PER_HR / 60.0


def compute_costs(total_seconds):
    total_minutes = total_seconds / 60.0
    base_minutes = min(total_minutes, SHIFT_MINUTES)
    overtime_minutes = max(total_minutes - SHIFT_MINUTES, 0.0)
    base_cost = base_minutes * BASE_RATE_PER_MIN
    overtime_cost = overtime_minutes * OT_RATE_PER_MIN
    total_cost = base_cost + overtime_cost
    return base_minutes, overtime_minutes, base_cost, overtime_cost, total_cost


def save_csvs_with_costs(
    tours, lookup, demand, full_out_csv, slim_out_csv, unload_minutes_per_box=15
):
    rows = []
    slim_rows = []
    for path in tours:
        travel_sec = compute_travel_seconds(path, lookup)
        if travel_sec is None:
            continue

        unloading_sec = compute_unloading_seconds(
            path,
            demand,
            depot_name="Centre Port",
            unload_minutes_per_box=unload_minutes_per_box,
        )
        total_sec = travel_sec + unloading_sec
        base_min, ot_min, base_cost, ot_cost, total_cost = compute_costs(total_sec)

        rows.append(
            {
                "route": "->".join(path),
                "travel_seconds": travel_sec,
                "unloading_seconds": unloading_sec,
                "total_time_seconds": total_sec,
                "total_time_minutes": total_sec / 60.0,
                "base_minutes_billed": base_min,
                "overtime_minutes_billed": ot_min,
                "base_cost": base_cost,
                "overtime_cost": ot_cost,
                "total_cost": total_cost,
            }
        )
        slim_rows.append(
            {
                "route": "->".join(path),
                "total_cost": total_cost,
            }
        )

    # Save both
    pd.DataFrame(rows).to_csv(full_out_csv, index=False)
    pd.DataFrame(slim_rows).to_csv(slim_out_csv, index=False)


if __name__ == "__main__":
    nodes = {
        "FreshChoice Cannons Creek",
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
        "Centre Port",
    }
    start = "Centre Port"
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
        "Centre Port": 0,
    }

    matrix_csv = Path("WoolworthsDurations2025.csv")
    max_demand_standard = 9
    max_demand_extra = 4
    max_intermediate = 4
    lookup = build_lookup(matrix_csv)

    # CSV for standard
    tours_std = generate_tours(
        nodes, demand_weekdays, start, max_demand_standard, max_intermediate
    )
    save_csvs_with_costs(
        tours_std,
        lookup,
        demand_weekdays,
        "Routes with Duration & per box - Standard.csv",
        "Route and Total Cost - Standard.csv",
        unload_minutes_per_box=15,
    )

    # CSV for extra
    tours_extra = generate_tours(
        nodes, demand_weekdays, start, max_demand_extra, max_intermediate
    )
    save_csvs_with_costs(
        tours_extra,
        lookup,
        demand_weekdays,
        "Routes with Duration & per box - Extra.csv",
        "Route and Total Cost - Extra.csv",
        unload_minutes_per_box=15,
    )
