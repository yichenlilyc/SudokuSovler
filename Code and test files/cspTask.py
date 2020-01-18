import random
import sys

class CSP():
    """The abstract class for a csp."""

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP . If variables is empty, it becomes domains.keys()."""

        variables = variables or list(domains.keys())

        self.variables = variables

        self.domains = domains

        self.neighbors = neighbors

        self.constraints = constraints

        self.initial = ()

        self.curr_domains = None

        self.nassigns = 0

        self.numassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""

        assignment[var] = val

        self.nassigns += 1
        self.numassigns = len(assignment)

        print(" ")

        for l in range(self.nassigns+1):
            print(" ", end="")
        print("Add variable and value: {", var, ":", val, "} to assignment. ")

        # for l in range(self.nassigns+1):
        #     print(" ", end="")
        # print("Now assignment:", assignment)
        self.display(own="Assign", assignment=assignment)

    def undoassign(self, var, assignment):
        """Remove {var: val} from assignment."""

        for l in range(self.nassigns + 2):
            print(" ", end="")

        self.nassigns -= 1

        if var in assignment:

            print("Remove {", var, ":", assignment[var], "} from assignment and backtrack to level", self.nassigns)

            del assignment[var]

            self.numassigns = len(assignment)

    def num_conflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently

        def conflict(var2):
            return (var2 in assignment and

                    not self.constraints(var, val, var2, assignment[var2]))

        return sum(conflict(v) for v in self.neighbors[var])

    def display(self, own="", assignment={}):
        """Show a human-readable representation of the CSP."""

        print('CSP:', self, 'assignment:', assignment)

    def init_curr_domains(self):

        """  """

        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def change_curr_domains(self, var, value):

        """Remove curr_domains to removals and change curr_domains of var from assuming var=value."""

        self.init_curr_domains()

        removals = [(var, a) for a in self.curr_domains[var] if a != value]

        self.curr_domains[var] = [value]

        return removals

    def prune(self, var, value, removals):

        """Delete var=value from curr_domains."""

        self.curr_domains[var].remove(value)

        if removals is not None:
            removals.append((var, value))

    def restore(self, removals):

        """Undo and restore curr_domains from removals."""

        for B, b in removals:
            self.curr_domains[B].append(b)

    def first_assignment(self):
        """Return the partial assignment implied by the current inferences."""

        self.init_curr_domains()

        assignment = {v: self.curr_domains[v][0]

                for v in self.variables if 1 == len(self.curr_domains[v])}

        self.numassigns = len(assignment)

        return assignment

    def goal_test(self, state):

            """The goal is to assign all variables, with all constraints satisfied."""

            if state:

                assignment = dict(state)

                return (len(assignment) == len(self.variables)

                        and all(self.num_conflicts(variables, assignment[variables], assignment) == 0

                                for variables in self.variables))

            else:

                return False

# ______________________________________________________________________________

# Constraint Propagation with AC-3


def AC3(csp, queue=None, removals=None):

    """[Figure 6.3]"""

    num_revised = 0
    revised = False
    bstr = " "

    for l in range(csp.nassigns + 1):
        bstr += " "

    csp.display(own="inference-mac-AC3", curr_domains=csp.curr_domains, removals=removals)

    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]

    csp.init_curr_domains()

    while queue:

        (Xi, Xj) = queue.pop()

        revised = revise(csp, Xi, Xj, removals)

        num_revised = num_revised + revised

        if revised:

            if not csp.curr_domains[Xi]:
                print(bstr, "infernce False!")
                return False

            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))

    print(bstr, "Number_revised:", num_revised)

    if num_revised:

        #print(bstr, "Inference pruned:", removals[-num_revised:])

        # print(bstr, 'After pruned curr_domains:')

        # for key in csp.curr_domains:
        #
        #     print(bstr, key, ":", csp.curr_domains[key])
        if csp.goal_test(csp.first_assignment()):

            csp.display(own="Result, Goal reached!", assignment=csp.first_assignment(), curr_domains={})

        else:

            csp.display(own="After pruned curr_domains", curr_domains=csp.curr_domains, removals=removals)

    else:

        print(bstr, "No pruned in this inference!")

    return True


def revise(csp, Xi, Xj, removals):

    """Return number of value we remove."""

    num_revised = 0

    for x in csp.curr_domains[Xi][:]:

        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x

        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):

            csp.prune(Xi, x, removals)

            num_revised += 1

    return num_revised


# ______________________________________________________________________________

# CSP Backtracking Search


# Variable ordering


def first_unassigned_variable(assignment, csp):

    """The default variable order."""

    return [var for var in csp.variables if var not in assignment][0]


def mrv_degree(assignment, csp):

    """Minimum-remaining-values heuristic, degree break tie"""

    mrvd_d = dict([(var, num_legal_values(csp, var, assignment)) for var in csp.variables if var not in assignment])

    mrvd_order = sorted(mrvd_d.items(), key=lambda d: d[1])

    mrvmin = mrvd_order[0][1]

    mrvdmaxvar = max([v for (v, value) in mrvd_order if value == mrvmin], key=lambda v: len(csp.neighbors[v]))

    csp.display(own="Variable select with mrv_degree", assignment={}, curr_domains=csp.curr_domains)

    print(" ")
    for l in range(csp.nassigns + 2):
        print(" ", end="")

    print("Select mrv_maxdegree variable:", mrvdmaxvar, "...mrv degree:", mrvmin, " ", len(csp.neighbors[mrvdmaxvar]))

    return mrvdmaxvar

def mrv_maxtlen(assignment, csp):

    """Minimum-remaining-values heuristic, max length task break tie"""

    nlv_d = dict([(var, num_legal_values(csp, var, assignment)) for var in csp.variables if var not in assignment])

    nlv_order = sorted(nlv_d.items(), key = lambda d:d[1])

    mrvmin = nlv_order[0][1]

    mrvmaxtlvar = max([v for (v, value) in nlv_order if value == mrvmin], key=lambda v:csp.variables[v])

    csp.display(own="Variable select with mrv_maxtlen", assignment=assignment, curr_domains=csp.curr_domains)

    print(" ")
    for l in range(len(assignment) + 2):
        print(" ", end="")

    print("Select variable of mrv and max length:", mrvmaxtlvar,
                            "...mrv maxl:", mrvmin, " ", csp.variables[mrvmaxtlvar])

    return mrvmaxtlvar


def num_legal_values(csp, var, assignment):

    if csp.curr_domains:

        return len(csp.curr_domains[var])

    else:

        return sum(csp.num_conflicts(var, val, assignment) == 0

                     for val in csp.domains[var])


# Value ordering


def unordered_domain_values(var, assignment, csp):

    """The default value order."""

    return (csp.curr_domains or csp.domains)[var]


def lcv(var, assignment, csp):

    """Least-constraining-values heuristic."""

    lcvorder= sorted((csp.curr_domains or csp.domains)[var],

                  key=lambda val: sum(not csp.constraints(var, val, var2, y) for var2 in csp.neighbors[var]
                                      for y in (csp.curr_domains or csp.domains)[var2]))

    # csp.num_conflicts(var, val, assignment) +

    csp.display(own="select value in order of lcv", assignment={},  curr_domains=csp.curr_domains)

    print(" ")

    for l in range(csp.nassigns + 2):
        print(" ", end="")

    print("lcv order of", "variable", var, ":", lcvorder)

    return lcvorder


def minpcost(var, assignment, csp):

    """Least-constraining-values heuristic."""

    minpcostorder = sorted((csp.curr_domains or csp.domains)[var],

                      key=lambda pcost: csp.pandcs[pcost])

    # lcvorder= sorted((csp.curr_domains or csp.domains)[var],
    #
    #               key=lambda val: csp.num_conflicts(var, val, assignment))

    csp.display(own="select value in order of minpcost", assignment=assignment,  curr_domains=csp.curr_domains)

    print(" ")

    for l in range(len(assignment) + 2):
        print(" ", end="")

    print("minpcost order of", "variable", var, ":", minpcostorder)

    return minpcostorder


# Inference


def no_inference(csp, var, value, assignment, removals):

    return True


def mac(csp, var, value, assignment, removals):

    """Maintain arc consistency."""

    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)


# The search, proper


def backtracking_search(csp,

                        select_unassigned_variable=first_unassigned_variable,

                        order_domain_values=unordered_domain_values,

                        inference=no_inference):

    """[Figure 6.5]"""

    def backtrack(assignment):

        if len(assignment) == len(csp.variables):

            return assignment

        var = select_unassigned_variable(assignment, csp)

        for value in order_domain_values(var, assignment, csp):

            if 0 == csp.num_conflicts(var, value, assignment):

                csp.assign(var, value, assignment)

                removals = csp.change_curr_domains(var, value)

                if inference(csp, var, value, assignment, removals):

                    result = backtrack(assignment)

                    if result is not None:
                        return result

                csp.undoassign(var, assignment)

                csp.restore(removals)

                csp.display(own="backtrack", assignment=assignment, curr_domains=csp.curr_domains)

        return None

    result = backtrack(csp.first_assignment())

    if csp.goal_test(result):

        csp.display(own="Result, Goal reached!", assignment=result, curr_domains={})

    else:

        print(" ")
        print("NO such assignment is possible")

    return result


# -----------------------------------------------------------------------------------------









