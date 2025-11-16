"""
Traveling Salesman Problem (TSP) Solver

This file runs independently of the main project skeleton
to solve the weighted TSP problem.

It reads 'hamilton_input_weighted.cnf' and finds the
minimum weight Hamiltonian cycle.
"""

import itertools
import time
from typing import List, Tuple, Set, Dict


def parse_weighted_graph_file(filename: str) -> List[Dict]:
    #Parses the weighted graph file and stores all instances.
    all_graphs = []
    current_graph_data = {}
    
    with open(filename, mode='r') as file: #read the file
        for line_content in file:
            parts = line_content.strip().split()
            
            if not parts:
                continue  # Skip empty lines
            
            line_type = parts[0]
            
            if line_type == 'c':
                # Comment line, signals start of a new instance
                if current_graph_data:
                    all_graphs.append(current_graph_data)
                
                instance_num = int(parts[2])
                current_graph_data = {
                    'id': instance_num,
                    'vertices': set(),
                    'edges': []
                }
            
            elif line_type == 'p':
                # Problem line: p edge num_vertices num_edges
                if current_graph_data:
                    num_vertices = int(parts[2])
                    current_graph_data['vertices'] = set(range(1, num_vertices + 1))
                        
            elif line_type == 'e':
                # Edge line: e v1 v2 weight
                if current_graph_data:
                    v1 = int(parts[1])
                    v2 = int(parts[2])
                    weight = int(parts[3])
                    
                    # Add the edge with its weight
                    current_graph_data['edges'].append((v1, v2, weight))

    # Add the last graph to the list
    if current_graph_data:
        all_graphs.append(current_graph_data)
        
    return all_graphs


# Helper & Algorithm Functions
def _build_adj_list(vertices: Set[int], edges: List[Tuple[int, int, int]]) -> Dict[int, Dict[int, int]]:
    #Helper function to build a weighted adjacency list
    #for efficient lookups.
    adj_list = {v: {} for v in vertices}
    for u, v, weight in edges:
        adj_list[u][v] = weight
        adj_list[v][u] = weight
    return adj_list

def tsp_bruteforce(
    vertices: Set[int], edges: List[Tuple[int, int, int]]
) -> Tuple[float, List[int]]:
    
   # Solves TSP using Brute Force.
   # Checks every possible permutation of vertices.
   
    adj_list = _build_adj_list(vertices, edges)
    start_node = 1
    other_nodes = [v for v in vertices if v != start_node]
    
    min_weight = float('inf')
    best_cycle = None

    for p in itertools.permutations(other_nodes): #go through all permuatiosn
        current_weight = 0
        current_node = start_node
        is_valid_cycle = True
        
        for next_node in p:
            if next_node in adj_list[current_node]:
                current_weight += adj_list[current_node][next_node]
                current_node = next_node
            else:
                is_valid_cycle = False
                break
        
        if not is_valid_cycle:
            continue
            
        if start_node in adj_list[current_node]:
            current_weight += adj_list[current_node][start_node]
        else:
            is_valid_cycle = False
            continue

        if current_weight < min_weight:
            min_weight = current_weight
            best_cycle = [start_node] + list(p) + [start_node]

    return min_weight, best_cycle #return bruteforce results


# Use global vars for the recursive backtracking function
min_weight_global = float('inf')
best_cycle_global = None
adj_list_global = {}
num_vertices_global = 0
start_node_global = 1

def _tsp_backtracking_recursive(current_node: int, current_weight: float, path: List[int]):
    #Recursive helper for the backtracking solver
    
    global min_weight_global, best_cycle_global
    
    # This where we ant to implemnent pruning
    if current_weight >= min_weight_global:
        return

    #Base Case
    if len(path) == num_vertices_global:
        if start_node_global in adj_list_global[current_node]:
            final_weight = current_weight + adj_list_global[current_node][start_node_global]
            
            if final_weight < min_weight_global:
                min_weight_global = final_weight
                best_cycle_global = path + [start_node_global]
        return

    #use recursion to explore nearest neighbors
    for neighbor, weight in adj_list_global[current_node].items():
        if neighbor not in path:
            path.append(neighbor) # Add to path
            _tsp_backtracking_recursive( 
                current_node=neighbor,
                current_weight=current_weight + weight,
                path=path
            )
            path.pop() # Backtrack

def tsp_backtracking(
    vertices: Set[int], edges: List[Tuple[int, int, int]]
) -> Tuple[float, List[int]]:
    #Solves TSP using backtracking with pruning.
    
    global min_weight_global, best_cycle_global, adj_list_global
    global num_vertices_global, start_node_global
    
    # Reset global state for this run
    adj_list_global = _build_adj_list(vertices, edges)
    num_vertices_global = len(vertices)
    min_weight_global = float('inf')
    best_cycle_global = None
    start_node_global = 1
    
    # Start the recursive search
    _tsp_backtracking_recursive(start_node_global, 0, [start_node_global])
    
    return min_weight_global, best_cycle_global

#main
if __name__ == "__main__":
    
    #set path name to read cnf file from input
    INPUT_FILE = 'input/hamilton_input_weighted.cnf'
    
    graphs = parse_weighted_graph_file(INPUT_FILE)
    
    if not graphs:
        print(f"No graphs found or file could not be read from {INPUT_FILE}")
    else:
        print(f"--- Solving TSP for {len(graphs)} instances ---")
        
        for graph in graphs:
            print(f"\n=== Instance {graph['id']} ===")
            vertices = graph['vertices']
            edges = graph['edges']
            
            #Run Brute Force
            print("Running Brute Force...")
            t0 = time.perf_counter()
            bf_weight, bf_cycle = tsp_bruteforce(vertices, edges)
            bf_time = time.perf_counter() - t0
            
            if bf_cycle:
                print(f"  [Brute Force]   Found cycle: {bf_cycle}")
                print(f"  [Brute Force]   Min Weight:  {bf_weight}")
            else:
                print("  [Brute Force]   No cycle found.")
            print(f"  [Brute Force]   Time: {bf_time:.6f}s")
            
            #Run Backtracking
            print("Running Backtracking...")
            t0 = time.perf_counter()
            bt_weight, bt_cycle = tsp_backtracking(vertices, edges)
            bt_time = time.perf_counter() - t0
            
            if bt_cycle:
                print(f"  [Backtracking]  Found cycle: {bt_cycle}")
                print(f"  [Backtracking]  Min Weight:  {bt_weight}")
            else:
                print("  [Backtracking]  No cycle found.")
            print(f"  [Backtracking]  Time: {bt_time:.6f}s")