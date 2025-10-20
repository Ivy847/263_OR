# Compare daily logistics cost for Woolworths fleet sizes (4, 3, 2) with SUB60 overflow.

fleet_sizes = [2, 3, 4]                          
costs_by_fleet = {v: [] for v in fleet_sizes}     

# Re-run the same day simulation loop but also compute SUB60 overflow costs, minimally inline.
import math

# Reuse the same parameters already defined above:
# - routes, index, get_cost, find_duration_simulation
# - weekday_demand_distribution, durations (from ORS), mu/sigma/low/high, etc.

N_RUNS = 1000  # increase runs for clearer boxplots
for _ in range(N_RUNS):
    rng = np.random.default_rng()
    mult = rng.lognormal(mean=mu, sigma=sigma, size=durations.shape)
    mult = np.clip(mult, low, high)
    var_durations = pd.DataFrame(durations.to_numpy() * mult, index=durations.index, columns=durations.columns)
    demands = bootstrap_weekday_demand(weekday_demand_distribution)

    # Partition routes by feasibility (<= 9 boxes = in-house feasible)
    route_names_working = []
    total_demand_working = []
    route_names_not = []
    total_demand_not = []

    for route in routes:
        d = 0.0
        for store in route:
            d += demands[store]
        name = "->".join(route)
        if d <= 9:
            route_names_working.append(name)
            total_demand_working.append(d)
        else:
            route_names_not.append(name)
            total_demand_not.append(d)

    # Durations (drive + service) for both sets 
    dur_working = find_duration_simulation(route_names_working, var_durations, index, total_demand_working) if route_names_working else np.array([], dtype=float)
    dur_not     = find_duration_simulation(route_names_not,     var_durations, index, total_demand_not)     if route_names_not     else np.array([], dtype=float)

    # Helper: SUB60 cost inline (no new function definitions)
    # Conservative: ceil(d/4) vans; each van does full route drive time + its own unload; $1000/4h blocks.
    def _sub60_cost_array(durations_sec, demands_arr):
        if len(durations_sec) == 0:
            return 0.0
        BOX_SERVICE = 15 * 60.0
        BLOCK_SEC = 4 * 60 * 60.0
        total = 0.0
        for dur, d in zip(durations_sec, demands_arr):
            drive = max(0.0, dur - d * BOX_SERVICE)           
            n_vans = int(math.ceil(d / 4.0))
            boxes_per_van = int(math.ceil(d / max(1, n_vans)))
            duty_per_van = drive + boxes_per_van * BOX_SERVICE
            blocks = int(math.ceil(duty_per_van / BLOCK_SEC))
            total += n_vans * (blocks * 1000.0)
        return total

    # For each fleet size, allocate up to (vans*2) longest feasible routes to in-house;
    # overflow + all infeasible routes go to SUB60.
    for vans in fleet_sizes:
        capacity = vans * 2
        if len(dur_working) > 0:
            order = np.argsort(-dur_working)  # longest first (minimises SUB60 under block pricing)
            inhouse_idx  = order[:min(capacity, len(order))]
            overflow_idx = order[min(capacity, len(order)):]
            inhouse_cost = np.sum(get_cost(dur_working[inhouse_idx])) if len(inhouse_idx) else 0.0
            overflow_cost = _sub60_cost_array(dur_working[overflow_idx], np.array(total_demand_working)[overflow_idx]) if len(overflow_idx) else 0.0
        else:
            inhouse_cost = 0.0
            overflow_cost = 0.0

        not_cost = _sub60_cost_array(dur_not, np.array(total_demand_not)) if len(dur_not) else 0.0
        total_day_cost = float(inhouse_cost + overflow_cost + not_cost)
        costs_by_fleet[vans].append(total_day_cost)

# Convert to arrays for plotting + stats
for v in fleet_sizes:
    costs_by_fleet[v] = np.array(costs_by_fleet[v], dtype=float)

# Boxplots with mean labels
import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))
data = [costs_by_fleet[v] for v in fleet_sizes]
labels = [f"{v} vans" for v in fleet_sizes]
bp = plt.boxplot(
    data, labels=labels, showmeans=True, meanline=True,
    meanprops={"color": "red", "linewidth": 2},
    medianprops={"color": "black"},
    patch_artist=True,
)
for patch in bp["boxes"]:
    patch.set_alpha(0.3)

means = [float(np.mean(costs_by_fleet[v])) for v in fleet_sizes]
ymax = max(means) if means else 0.0
for i, m in enumerate(means, start=1):
    plt.text(i, m + 0.02 * ymax, f"${m:,.0f}", ha="center", va="bottom", color="red", fontsize=10, fontweight="bold")

plt.title("Daily Logistics Cost vs In-house Fleet Size (SUB60 handles overflow)")
plt.ylabel("Total daily logistics cost ($)")
plt.xlabel("Woolworths vans (2 shifts/van/day)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Mean trend line
plt.figure(figsize=(8, 4))
plt.plot(fleet_sizes, means, marker="o")
for x, y in zip(fleet_sizes, means):
    plt.text(x, y, f"${y:,.0f}", ha="center", va="bottom", fontsize=9)

    import matplotlib.ticker as mticker

    plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(integer=True))


plt.title("Mean Daily Cost vs Fleet Size (fewer vans ⇒ higher cost)")
plt.xlabel("Woolworths vans")
plt.ylabel("Mean daily logistics cost ($)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# summary
print("\n--- Fleet Size Scenario Summary (SUB60 overflow) ---")
for v in fleet_sizes:
    arr = costs_by_fleet[v]
    print(f"{v} vans: mean ${np.mean(arr):,.0f}, std {np.std(arr, ddof=1):,.0f}, "
          f"p50 ${np.percentile(arr,50):,.0f}, p90 ${np.percentile(arr,90):,.0f}, max ${np.max(arr):,.0f}")


