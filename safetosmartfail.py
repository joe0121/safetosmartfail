import sys

def run_smartfail_calculator():
    protections = [
        {"name": "+1n", "min_nodes": 2},
        {"name": "+2d:1n", "min_nodes": 3},
        {"name": "+2n", "min_nodes": 3},
        {"name": "+3d:1n", "min_nodes": 4},
        {"name": "+3d:1n1d", "min_nodes": 4},
        {"name": "+3n", "min_nodes": 4},
        {"name": "+4d:1n", "min_nodes": 5},
        {"name": "+4d:2n", "min_nodes": 5},
        {"name": "+4n", "min_nodes": 5}
    ]

    print("--- Isilon SmartFail Safety Calculator ---")
    
    # 1. User Selection
    for i, p in enumerate(protections, 1):
        print(f"{i}) {p['name']}")
    
    try:
        choice = int(input("\nSelect Protection Level (Number): "))
        selected_prot = protections[choice - 1]
        
        nodes = int(input("Current number of nodes in pool: "))
        used_tb = float(input("Current USED capacity in pool (TiB): "))
        total_tb = float(input("Total RAW capacity of pool (TiB): "))
    except (ValueError, IndexError):
        print("Error: Please enter valid numbers.")
        return

    # 2. The Math
    # Calculate raw capacity per node to see what is lost
    avg_node_raw = total_tb / nodes
    remaining_raw_capacity = total_tb - avg_node_raw
    
    # Calculate utilization after data moves to remaining nodes
    projected_util = (used_tb / remaining_raw_capacity) * 100
    remaining_nodes = nodes - 1
    
    # Calculate Cleanup Targets
    # To reach 85% safety:
    cleanup_to_85 = used_tb - (remaining_raw_capacity * 0.85)
    # To reach 90% absolute limit:
    cleanup_to_90 = used_tb - (remaining_raw_capacity * 0.90)

    # 3. Decision Engine
    print("\n" + "="*50)
    print(f"ANALYSIS FOR REMOVING 1 NODE")
    print(f"Projected Utilization: {projected_util:.2f}%")
    print(f"Nodes Remaining:       {remaining_nodes} (Min: {selected_prot['min_nodes']})")
    print("-" * 50)

    # Protection Check First
    if remaining_nodes < selected_prot['min_nodes']:
        print("\033[91m[!!] UNSAFE: NODE COUNT CRITICAL\033[0m")
        print(f"Removing a node drops the pool to {remaining_nodes} nodes.")
        print(f"The {selected_prot['name']} policy requires at least {selected_prot['min_nodes']} nodes.")
        return

    # Capacity Logic (Your specific thresholds)
    if projected_util >= 90:
        print("\033[91m[!!] UNSAFE: DO NOT PERFORM SMARTFAIL\033[0m")
        print(f"Utilization will hit {projected_util:.2f}%.")
        print(f"RECOMMENDATION: Clear at least {cleanup_to_90:.2f} TiB before starting.")
    
    elif projected_util >= 85:
        print("\033[93m[!] CAUTION: HIGH UTILIZATION\033[0m")
        print(f"Utilization will hit {projected_util:.2f}%.")
        print(f"RECOMMENDATION: Clear space if possible (approx {cleanup_to_85:.2f} TiB) to ensure a healthy re-protect.")
    
    else:
        print("\033[92m[✓] SAFE TO PROCEED\033[0m")
        print(f"Pool will be at {projected_util:.2f}% which is within safe limits.")

    print("="*50)

if __name__ == "__main__":
    run_smartfail_calculator()