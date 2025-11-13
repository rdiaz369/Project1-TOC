"""
Hamilton Cycle Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c INSTANCE 1
p edge 4 5
e 1 2
e 1 4
e 2 3
e 2 4
e 3 4

c INSTANCE 2
p edge 6 10
e 1 5
e 1 6
e 2 3
e 2 4
e 2 6
e 3 4
e 3 5
e 3 6
e 4 5
e 4 6

c INSTANCE 3
p edge 5 4
e 1 5
e 2 3
e 3 5
e 4 5


OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id, n_vertices, n_edges, k, method, colorable, time_seconds, coloring

EXAMPLE OUTPUT
--------------
Instance_ID,Num_Vertices,Num_Edges,Hamiltonian_Path,Hamiltonian_Cycle,Largest_Cycle_Size,Algorithm,Time
1,4,5,"[1, 2, 3, 4]","[1, 2, 3, 4, 1]",4,"BruteForce",0.000000
2,6,10,"[1, 5, 3, 2, 4, 6]","[1, 5, 3, 2, 4, 6, 1]",6,"BruteForce",0.000000
3,5,4,None,None,0,"BruteForce",0.000000

"""

import itertools
from typing import List, Tuple, Set, Dict

from src.helpers.hamilton_cycle_helper import HamiltonCycleAbstractClass


class HamiltonCycleColoring(HamiltonCycleAbstractClass):
    """
    NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
    For this you dont need to save anything just make sure to return exact related output.

    For ease look at the Abstract Solver class and basically we are having the run method which does the saving
    of the CSV file just focus on the logic
    """

    #Make a new helper method to construct an unweighted adjacency set
    def _build_adj_set(self, vertices: Set[int], edges: List[Tuple[int]]) -> Dict[int, Set[int]]:
        
        adj_set = {v: set() for v in vertices}
        #here the edges willb be in unweighted tuples (u,v)
        for u, v in edges:
            if u in adj_set and v in adj_set:
                adj_set[u].add(v)
                adj_set[v].add(u)
        return adj_set

    def hamilton_backtracking(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:        
        # return (path_exists, path, cycle_exists, cycle, largest)
        pass

    def hamilton_bruteforce(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        
        adj_set = self._build_adj_set(vertices, edges)
        n = len(vertices)
        
        found_path = None
        found_cycle = None
        largest_cycle_size = 0 #this would be our best case 
        
        #
        for p in itertools.permutations(sorted(list(vertices))): #go through all permutaions
            is_path = True
            #lets checkk if its a valid path
            for i in range(n-1):
                if p[i+1] not in adj_set[p[i]]:
                    is_path = False
                    break
            
            
            if is_path: #then we have found our Hamiltonian Path
                if not found_path:
                    found_path = list(p)
                    
                # next we need to check if the path is also a cycle
                if p[0] in adj_set[p[-1]]:
                    found_cycle = list(p) + [p[0]]
                    largest_cycle_size = n #if it reaches the start then it is the largest
                    return (True, found_path, True, found_cycle, largest_cycle_size) # if we found both we can return early
                
        # need if statement for whren we finish the loop and found a path, but no cycle
        if found_path and not found_cycle: #heere we must have found the best case for unwieghted
            
            return (True, found_path, False, None, 0)
        
        #NO PATH or cycle found
        return (False, None, False, None, 0)

    def hamilton_simple(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass

    def hamilton_bestcase(
        self, vertices: set, edges: List[Tuple[int]]
    ) -> Tuple[bool, List[int], bool, List[int], int]:
        pass
