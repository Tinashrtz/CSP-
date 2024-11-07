from collections import deque
from typing import Callable, List, Tuple
from CSP import CSP



class Solver(object):

    def __init__(self, csp: CSP, domain_heuristics: bool = False, variable_heuristics: bool = False, AC_3: bool = False) -> None:
        """
        Initializes a Solver object.

        Args:
            csp (CSP): The Constraint Satisfaction Problem to be solved.
            domain_heuristics (bool, optional): Flag indicating whether to use domain heuristics. Defaults to False.
            variable_heuristics (bool, optional): Flag indicating whether to use variable heuristics. Defaults to False.
            AC_3 (bool, optional): Flag indicating whether to use the AC-3 algorithm. Defaults to False.
        """
        self.csp = csp
        self.domain_heuristic = domain_heuristics
        self.variable_heuristic = variable_heuristics
        self.AC_3 = AC_3
    
    
    
    def backtrack_solver(self) -> List[Tuple[str, str]]:
        """
        Backtracking algorithm to solve the constraint satisfaction problem (CSP).

        Returns:
            List[Tuple[str, str]]: A list of variable-value assignments that satisfy all constraints.
        """ 

        if self.csp.is_complete():
            return self.csp.assignments
        var = self.select_unassigned_variable()
        for value in self.ordered_domain_value(var):
            if self.csp.is_consistent(var,value):
                
                removed_domain =[]
                for i in self.csp.variables[var]:
                    if i != value:
                        removed_domain.append((var, i))
                
                self.csp.assign(var,value)
                
                if self.AC_3:
                    ac3_out = self.apply_AC3()
                    removed_domain.extend(ac3_out)
                # print(self.csp.assignments_number)
                result = self.backtrack_solver()
                if result:
                    return result
                #self.csp.unassign([(value, [value])], var)      
                self.csp.unassign(removed_values_from_domain = removed_domain, variable = var)
                                        
            
        return None


        

    def select_unassigned_variable(self) -> str:                             ##okay
        """
        Selects an unassigned variable using the MRV heuristic.

        Returns:
            str: The selected unassigned variable.
        """
        if self.variable_heuristic:
            return self.MRV()
        return self.csp.unassigned_var[0]


       

    def ordered_domain_value(self, variable: str) -> List[str]:                   ##okay
        """
        Returns a list of domain values for the given variable in a specific order.

        Args:
            variable (str): The name of the variable.

        Returns:
            List[str]: A list of domain values for the variable in a specific order.
        """
        
        if self.domain_heuristic:
            return self.LCV(variable)
        return self.csp.variables[variable]



        
    def arc_reduce(self, x, y, consistent) -> List[str]:                              
        """
        Reduce the domain of variable x based on the constraints between x and y.

        Parameters:
        - x: The first variable.
        - y: The second variable.
        - consistent: A function that checks the consistency between two values.

        Returns:
        - The reduced domain of variable x if the domain is reduced, None otherwise.
        """
        domain_reduced = False                              
        domain_x = self.csp.variables[x]
        domain_y = self.csp.variables[y]
        
        removed=[]

        for val_x in domain_x:
           if not any(consistent(val_x, val_y) for val_y in domain_y):
               removed.append((x, val_x))
               domain_x.remove(val_x)
               domain_reduced = True

        return removed if domain_reduced else None
    
    
        

    def consistent(self, value_x: str, value_y: str) -> bool:                   
        return value_x != value_y  # Values are consistent if they are not equal
    
    
   
   
    def apply_AC3(self) -> List[Tuple[str, str]]:
        """
        Applies the AC3 algorithm to reduce the domains of variables in the CSP.

        Returns:
            A list of tuples representing the removed values from the domain of variables.
        """
        queue = deque(self.csp.constraints)  # Initialize queue with all arcs
        removed_values = []  # List to store removed values

        while queue:
            arc = queue.pop()
            # print(self, arc)
            rv = self.arc_reduce(arc[0], arc[1], self.consistent)
            if rv != None: # equal to reducing
                removed_values.extend(rv)  # If domain is reduced, add to removed values list

                for func, neighbor in self.csp.var_constraints[arc[0]]:
                    if neighbor != arc[1]:
                        queue.append((neighbor, arc[0]))  # Add arcs (neighbor, X_i) to the queue

        return removed_values


    def MRV(self) -> str:                                                             
        """
        Selects the variable with the Minimum Remaining Values (MRV) heuristic.

        Returns:
            str: The variable with the fewest remaining values.
        """
        min_remaining_values = float('inf')
        selected_variable = None

        for variable in self.csp.unassigned_var:
            remaining_values = len(self.csp.variables[variable])
            if remaining_values < min_remaining_values:
                min_remaining_values = remaining_values
                selected_variable = variable

        return selected_variable
        
    

    def LCV(self, variable: str) -> List[str]:                                        
        """ 
        Orders the values of a variable based on the Least Constraining Value (LCV) heuristic.

        Args:
            variable (str): The variable for which to order the values.

        Returns:
            List[str]: A list of values sorted based on the number of constraints they impose.
        """
        #values = self.csp.variables[variable]
        values = self.csp.variables.get(variable, [])
        constraints_count = {value: 0 for value in values}

        for func, neighbor in self.csp.var_constraints[variable]:
            for value in values:
                if value in self.csp.variables[neighbor]:
                    constraints_count[value] += 1

        return sorted(values, key=lambda value: constraints_count[value])



