import argparse
from enum import Enum
from CSP import CSP
from Solver import Solver
from map_generator import generate_borders_by_continent
from graphics import draw
import random
from collections import deque
import matplotlib.pyplot as plt
import numpy as np


class Continent(Enum):
    asia = "Asia"
    africa = "Africa"
    america = "America"
    europe = "Europe"

    def __str__(self):
        return self.value
    

def main():
    """
    Main function to solve the map coloring problem using CSP.

    The function takes command-line arguments to customize the solving process.

    Command-line arguments:
    - -m, --map: Specify the map to solve the coloring problem on. Must be one of [Asia, Africa, America, Europe].
    - -lcv, --lcv: Enable least constraint value (LCV) as an order-type optimizer.
    - -mrv, --mrv: Enable minimum remaining values (MRV) as an order-type optimizer.
    - -ac3, --arc-consistency: Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution.
    - -ND, --Neighborhood-distance: The value determines the threshold for neighboring regions' similarity in color, with a default of 1 ensuring adjacent regions have distinct colors; increasing it, for instance to 2, extends this dissimilarity to the neighbors of neighbors.
    """
    parser = argparse.ArgumentParser(
        prog="Map Coloring",
        description="Utilizing CSP to solve map coloring problem",
    )

    parser.add_argument(
        "-m",
        "--map",
        type=Continent,
        choices=list(Continent),
        help="Map must be: [Asia, Africa, America, Europe]",
    )
    parser.add_argument(
        "-lcv",
        "--lcv",
        action="store_true",
        help="Enable least constraint value (LCV) as a order-type optimizer"
    )
    parser.add_argument(
        "-mrv",
        "--mrv",
        action="store_true",
        help="Enable minimum remaining values (MRV) as a order-type optimizer"
    )
    parser.add_argument(
        "-ac3",
        "--arc-consistency",
        action="store_true",
        help="Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution"
    )
    parser.add_argument(
        "-ND",
        "--Neighborhood-distance",
        type=int,
        default=1,
        help="The value determines the threshold for neighboring regions' similarity in color, with a default of 1 ensuring adjacent regions have distinct colors; increasing it, for instance to 2, extends this dissimilarity to the neighbors of neighbors."
    )
    
#defult Number of colors to generate
num_colors = 3

"""     # Generate num_colors random colors using a matplotlib color map
    cmap = plt.cm.get_cmap('tab20')  # You can choose any other color map as well
    random_colors_matplotlib = [cmap(i) for i in np.linspace(0, 1, num_colors)]
    #print(random_colors_matplotlib)
    
   
   
   
    def bfs_with_distance(graph, start, max_distance):
        visited = set()
        queue = [(start, 0)]
        neighbors_within_distance = []
        
        while queue:
            node, distance = queue.pop(0)
            if distance > max_distance:
                break
            if node not in visited:
                visited.add(node)
                if distance <= max_distance:
                    neighbors_within_distance.append(node)
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, distance + 1))
        
        return neighbors_within_distance """

   
   
args = parser.parse_args()
borders = generate_borders_by_continent(continent=str(args.map))
print(borders)
    
    
graph = borders
#handling missing countries
keys_to_add = []
for country, neighbors in graph.items():
    for neighbor in neighbors:
        if neighbor not in graph:
            keys_to_add.append(neighbor)
# Add the missing keys
for key in keys_to_add:
    graph[key] = []
        
    
                
    
"""     max_distance = args.Neighborhood_distance #based on client n
    #max_distance=
    
    results_dict = {}
    for country in graph:
        #results_dict[country] =bfs_with_distance(graph, country, max_distance)
        results_dict[country] = list(bfs_with_distance(graph, country, max_distance))
    
    # Remove the country from its own list of values 
    for country in borders :   
           results_dict[country].remove(country)
            

    
    # print("---------------------------")
    # print(results_dict)
 """
   
 
    
"""     # # Create a CSP instance with the generated borders
    csp = CSP()
    
    
    #init
    if max_distance == 1: 
        countries=list(borders.keys())
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        constraint_func = lambda x,y : x!= y
        for country in countries:
                neighbor_removed = []
                for neighbor in borders[country]:
                    if neighbor not in countries:
                        neighbor_removed.append(neighbor)
                    else:
                        csp.add_constraint(constraint_func,[country,neighbor])
                        csp.constraints.append((country,neighbor))

                borders[country] =[i for i in borders[country] if i not in neighbor_removed]
            
        for country in countries:
                csp.add_variable(country,["red","blue","green","yellow"])
                csp.assignments[country] = None
    
    else:
        countries=list(graph.keys())
        constraint_func = lambda x,y : x!= y
        for country in countries:
                neighbor_removed = []
                for neighbor in results_dict[country]:
                    if neighbor not in countries:
                        neighbor_removed.append(neighbor)
                    else:
                        csp.add_constraint(constraint_func,[country,neighbor])
                        csp.constraints.append((country,neighbor))

                results_dict[country] =[i for i in graph[country] if i not in neighbor_removed]
         
        result = None    
        while result == None :
            num_colors +=1
            for country in countries:
                csp.add_variable(country,[cmap(i) for i in np.linspace(0, 1, num_colors)])
                csp.assignments[country] = None
               
            solver = Solver(csp=csp,domain_heuristics=args.lcv,variable_heuristics=args.mrv,AC_3=args.arc_consistency)
            result = solver.backtrack_solver()
            if result != None :
                assignments_number = solver.csp.assignments_number
                finalresult = {}
                for i in result:
                    finalresult[i[0]] = i[1]
                print(" minimum needed colors:",num_colors)
                draw(solution=finalresult, continent=str(args.map), assignments_number=assignments_number) """
                
                
# Initialize a Solver object with the CSP and specified heuristic options
solver = Solver(csp=csp,domain_heuristics=args.lcv,variable_heuristics=args.mrv,AC_3=args.arc_consistency)
    
# # Solve the CSP
result = solver.backtrack_solver()
print(result)
   
# Retrieve the number of assignments made during the solving process
assignments_number = solver.csp.assignments_number

finalresult = {}
for i in result:
    finalresult[i[0]] = i[1]
    
    draw(solution=result, continent=str(args.map), assignments_number=assignments_number)
    


if __name__ == '__main__':
    main()