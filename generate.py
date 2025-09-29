import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("#", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to a text file.
        """
        letters = self.letter_grid(assignment)
        
        with open(filename, 'w') as f:
            for i in range(self.crossword.height):
                for j in range(self.crossword.width):
                    if self.crossword.structure[i][j]:
                        f.write(letters[i][j] or " ")
                    else:
                        f.write("#")
                f.write("\n")

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            # Keep only words that match the variable's length
            self.domains[var] = {
                word for word in self.domains[var] 
                if len(word) == var.length
            }

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get the overlap between x and y
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False  # No overlap, no revision needed
        
        i, j = overlap  # x[i] must equal y[j]
        
        # Keep only words in x's domain that have a compatible word in y's domain
        original_size = len(self.domains[x])
        
        self.domains[x] = {
            word_x for word_x in self.domains[x]
            if any(word_x[i] == word_y[j] for word_y in self.domains[y])
        }
        
        # Return True if domain was changed
        return len(self.domains[x]) < original_size

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initialize queue of arcs
        if arcs is None:
            # Start with all arcs in the problem
            queue = []
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x != y and self.crossword.overlaps[x, y] is not None:
                        queue.append((x, y))
        else:
            queue = list(arcs)
        
        # Process arcs until queue is empty
        while queue:
            x, y = queue.pop(0)
            
            # Make x arc consistent with y
            if self.revise(x, y):
                # If x's domain becomes empty, no solution exists
                if not self.domains[x]:
                    return False
                
                # Add arcs back to queue for neighbors of x (except y)
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if all variables in the crossword are assigned
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check that all words are distinct
        words = list(assignment.values())
        if len(words) != len(set(words)):
            return False
        
        # Check that all assigned words have correct length
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
        
        # Check binary constraints (overlaps)
        for var1, word1 in assignment.items():
            for var2, word2 in assignment.items():
                if var1 == var2:
                    continue
                
                overlap = self.crossword.overlaps[var1, var2]
                if overlap is not None:
                    i, j = overlap
                    if word1[i] != word2[j]:
                        return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Get unassigned neighbors
        unassigned_neighbors = [neighbor for neighbor in self.crossword.neighbors(var) 
                               if neighbor not in assignment]
        
        # If no unassigned neighbors, return domain values in any order
        if not unassigned_neighbors:
            return list(self.domains[var])
        
        # For each value in var's domain, count how many values it rules out for neighbors
        value_constraints = []
        for value in self.domains[var]:
            ruled_out_count = 0
            
            for neighbor in unassigned_neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap is not None:
                    i, j = overlap  # var[i] must equal neighbor[j]
                    for neighbor_value in self.domains[neighbor]:
                        if value[i] != neighbor_value[j]:
                            ruled_out_count += 1
            
            value_constraints.append((value, ruled_out_count))
        
        # Sort by least constraining (fewest values ruled out)
        value_constraints.sort(key=lambda x: x[1])
        
        return [value for value, _ in value_constraints]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Get all unassigned variables
        unassigned_vars = [var for var in self.crossword.variables if var not in assignment]
        
        if not unassigned_vars:
            return None
        
        # Calculate MRV and degree for each unassigned variable
        def get_priority(var):
            mrv = len(self.domains[var])  # Minimum remaining values
            # Degree heuristic: count unassigned neighbors
            unassigned_neighbors = len([neighbor for neighbor in self.crossword.neighbors(var) 
                                      if neighbor not in assignment])
            return (mrv, -unassigned_neighbors)  # Negative because we want highest degree first
        
        # Sort by MRV first, then by degree (highest degree first)
        unassigned_vars.sort(key=get_priority)
        
        return unassigned_vars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base case: if assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment
        
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)
        
        # Try each value in the variable's domain (ordered by heuristic)
        for value in self.order_domain_values(var, assignment):
            # Create a copy of assignment and assign the value
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            # Check if this assignment is consistent
            if self.consistent(new_assignment):
                # Recursively try to complete the assignment
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        
        # No valid assignment found
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
