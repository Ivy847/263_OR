import pulp
import pandas as pd
import math

# Load routes
std_routes = pd.read_csv("Route and Total Cost - Standard.csv")
sub_routes = pd.read_csv("Route and Total Cost - Extra.csv")

# Tag van types
std_routes["van_type"] = "WW"
sub_routes["van_type"] = "SUB60"

# For SUB60: flat $1000 per route
sub_routes["total_cost"] = 1000

# Merge into one dataframe
routes_df = pd.concat([std_routes, sub_routes], ignore_index=True)

# Build store set (exclude depot)
stores = set()
for r in routes_df["route"]:
    stops = r.split("->")
    for s in stops:
        if s not in ("Centre Port", "CentrePort Wellington"):
            stores.add(s)

R = list(routes_df["route"])
S = list(stores)

# Dicts
cost = routes_df.set_index("route")["total_cost"].to_dict()
van_type = routes_df.set_index("route")["van_type"].to_dict()

# parameters
ANNUAL_VAN_COST = 50000
WORKING_DAYS = 312

# Assumption: Woolworths vans are used ~6 days/week × 52 weeks = 312 working days per year
# Fixed daily van cost = 50,000 ÷ 312 ≈ 160 per van per day
DAILY_VAN_COST = ANNUAL_VAN_COST / WORKING_DAYS   # ≈160

# Assemble model
model = pulp.LpProblem("Woolworths_Van_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", R, cat="Binary")       # route chosen
V = pulp.LpVariable("Vans_retained", lowBound=0, cat="Integer")  # number of WW vans kept

# Objective: route costs + fixed daily van costs
model += pulp.lpSum(cost[r] * x[r] for r in R) + DAILY_VAN_COST * V, "TotalCost"

# Constraint (a): every store covered exactly once
for s in S:
    model += pulp.lpSum((s in r.split("->")) * x[r] for r in R) == 1, f"Cover_{s}"

# Constraint (b): WW van capacity (each van can do 2 routes)
model += pulp.lpSum(x[r] for r in R if van_type[r] == "WW") <= 2 * V, "WW_VanCapacity"

# Solve
solver = pulp.PULP_CBC_CMD(msg=True)
model.solve(solver)

# Display results
print("Status:", pulp.LpStatus[model.status])
print("Optimal cost:", pulp.value(model.objective))
print("Woolworths vans retained:", pulp.value(V))
print("\nChosen routes:")
for r in R:
    if pulp.value(x[r]) > 0.5:
        print(" -", r, "| Cost:", cost[r], "| Van type:", van_type[r])
