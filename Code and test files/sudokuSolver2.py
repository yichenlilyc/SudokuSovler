import  random
import sys
import numpy as np
from itertools import combinations

from cspTask import *


# -----------------------------------------------------------------------------------------

# Sudoku problem


class sudokuCSP(CSP):
    """The subclass  for a tasks schedule."""

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP . If variables is empty, it becomes domains.keys()."""
        super().__init__(variables, domains, neighbors, constraints)

        self.init_assignment = {}

    def L3D(self):

        CSP.init_curr_domains(self)

        for i in range(dimension):
            row = [str(i) + ',' + str(col) for col in range(dimension)]
            for comb3 in combinations(row,3):
                if set(self.curr_domains[comb3[0]])&set(self.curr_domains[comb3[1]])&set(self.curr_domains[comb3[2]]):
                    u = set(self.curr_domains[comb3[0]])|set(self.curr_domains[comb3[1]])|set(self.curr_domains[comb3[2]])
                    if len(u) == 3:
                        for r in (set(row) - set(comb3)):
                            # print("==== ",comb3, u, r, self.curr_domains[str(r)])
                            self.curr_domains[str(r)] = list(set(self.curr_domains[str(r)]) - u)
                            # print("==== ",comb3, u, r, self.curr_domains[str(r)])

        for j in range(dimension):
            col = [str(row) + ',' + str(j) for row in range(dimension)]
            for comb3 in combinations(col, 3):
                if set(self.curr_domains[comb3[0]]) & set(self.curr_domains[comb3[1]]) & set(
                        self.curr_domains[comb3[2]]):
                    u = set(self.curr_domains[comb3[0]]) | set(self.curr_domains[comb3[1]]) | set(
                        self.curr_domains[comb3[2]])
                    if len(u) == 3:
                        for r in (set(col) - set(comb3)):
                            # print("---- ", comb3, u, r, self.curr_domains[str(r)])
                            self.curr_domains[str(r)] = list(set(self.curr_domains[str(r)]) - u)
                            # print("---- ", comb3, u, r, self.curr_domains[str(r)])


    def display(self, own="revise", assignment={}, removals=[], curr_domains={}):
        """Show a human-readable representation of the CSP."""

        print(" ")
        hstr = ""
        bstr = ""
        strr="------+"
        for i in range(dimension_sqrt):
            if not i ==dimension_sqrt-1:
                strr+="------+"
            else:
                strr+="------"

        for l in range(self.nassigns + 1):
            hstr += "-"
            bstr += " "

        if own == "Initial state":
            print(own, '(num of assign:', len(assignment), '):')
        elif own == "Assign":
            print(hstr, 'Search level', self.nassigns)
            print(bstr, 'Current state', '(num of assign:', self.numassigns, "):")
        elif own == "Result, Goal reached!":
            print(bstr, "Goal reached! One of solution(num of assign:", len(assignment), '):')
        else:
            print(hstr, 'Search level', self.nassigns, '(num of assign:', self.numassigns, ")")

        print("")

        if assignment:

            print(bstr, strr)

            for row in range(dimension):

                print(' ', bstr, end="")

                for col in range(dimension):

                    if str(row) + ',' + str(col) in assignment.keys():
                        if str(row) + ',' + str(col) in self.init_assignment.keys():
                            print('\033[1m'+str(assignment[str(row) + ',' + str(col)])+'\033[0m', '', end="")
                        else:
                            print(assignment[str(row) + ',' + str(col)], '', end="")
                    else:
                        print('.', '', end="")

                    if (col + 1) % dimension_sqrt == 0 and col < dimension-1:
                        print('|', '',  end="")

                print("")

                if (row + 1) % dimension_sqrt == 0:
                    print(bstr, strr)

        if own not in ["Result, Goal reached!", "Initial state", "Assign"]:
            print(bstr, 'Now going to', own, ":")


def input_file():

    inputFile = input("Please input sudoku input file Name(sudoku1.txt): ")

    try:

        f = open(inputFile, 'r')
        #f = open("sudoku2.txt", 'r')

        fline = f.readlines()

        f.close()

        return fline

    except FileNotFoundError:

        print("File not found!")

def get_dimension(fline):
    dimension=len(fline)
    return dimension

fline = input_file()
dimension=get_dimension(fline)
dimension_sqrt=int(dimension**0.5)

def init_sudoku(fline):

    digit=[]
    # dimension=9
    # dimension_sqrt=int(dimension**0.5)
    sdk=np.zeros((1,dimension*dimension))
    line=[]

    for i in range(len(fline)):
        fline[i] = fline[i].split()
        for j in fline[i]:
            digit.append(int(j))

    for i in range(len(digit)):
        sdk[0,i]=digit[i]

    sudoku=np.reshape(sdk,(dimension,dimension))
    sudoku=sudoku.astype(int)
    print(sudoku)

    csgraph = {}
    do=[]
    domains={}
    vertex={}
    row=[]
    neighbor={}

    for i in range(dimension):
        do.append(i+1)
    print("--")
    print(do)

    for i in range(0,dimension):
        for j in range(0,dimension):
            vertex[str(i)+","+str(j)]=0
            #cs_dict.append(str(i)+","+str(j))
            domains[str(i)+","+str(j)] = []
            neighbor[str(i)+","+str(j)] = []
        # vertex.append(row)
        # row=[]
    print("vertex:")
    print(vertex)

    for x in range(dimension):
        for y in range(dimension):

            for col in range(dimension):
                if not [x,col]==[x,y]:
                    # neighbor[str(x)+","+ str(y)].append([x,col])
                    neighbor[str(x) + "," + str(y)].append(str(x)+","+str(col))
                    #neighbor[str(x) + "," + str(y)]=str(x) + "," + str(col)

            for row in range(dimension):
                if not [row,y]==[x,y]:
                    # neighbor[str(x)+","+ str(y)].append([row,y])
                    neighbor[str(x) + "," + str(y)].append(str(row) + "," + str(y))
                    #neighbor[str(x) + "," + str(y)] = str(row) + "," + str(y)

            for a in range(dimension_sqrt):
                for b in range(dimension_sqrt):
                    j=a+dimension_sqrt*(x//dimension_sqrt)
                    k=b+dimension_sqrt*(y//dimension_sqrt)
                    if not [j,k]==[x,y]:
                        # neighbor[str(x) +","+ str(y)].append([j,k])
                        neighbor[str(x) + "," + str(y)].append(str(j) + "," + str(k))
                       # neighbor[str(x) + "," + str(y)] = str(j) + "," + str(k)

    print("neighber:")
    print(neighbor)

    known={}
    for i in range(dimension):
        for j in range(dimension):
            if not sudoku[i,j]==0:
                domains[str(i)+","+str(j)].append(sudoku[i,j])
                # known.append([str(i)+","+str(j)])
                known[str(i)+","+str(j)]=sudoku[i,j]
            else:
                domains[str(i)+","+str(j)]=do
    print("domains:")
    print(domains)

    # for i in known.keys():
    #     for item in neighbor[i]:
    #         print(domains[item[0]])
    #         if known[i] in domains[item[0]]:
    #             temp=domains[item[0]]
    #
    #             temp.remove(known[i])
    #             print(temp)
    #             # domains[item]=temp
    #
    # print(domains)

    csgraph["domains"] = domains
    csgraph["vertex"] = vertex
    csgraph["neighbors"] = neighbor

    return csgraph



csgraph=init_sudoku(fline)


def sudoku_constraints(A, a, B, b):
    """Constraint is satisfied return true"""
    return a != b


sudokucsp = sudokuCSP(csgraph["vertex"], csgraph["domains"], csgraph["neighbors"], sudoku_constraints)

sudokucsp.init_assignment = sudokucsp.first_assignment()

sudokucsp.display(own="Initial state", assignment=sudokucsp.init_assignment)

AC3(sudokucsp)


if sudokucsp.goal_test(sudokucsp.first_assignment()):

    print("\nAC3 directly reach Goal!\n")
    print("system exit!")
    sys.exit(0)

sudokucsp.L3D()

sudokucsp.init_assignment = sudokucsp.first_assignment()

sudokucsp.display(own="After L3D state", assignment=sudokucsp.init_assignment)

print("  ")
print("Select:")

print("  1. no params backtracking_search.")
print("  2. backtracking_search with mrv_degree lcv mac-AC3.")
print("  0. exit.\n")

inputs = input("Please input your select number(1 or 2):")


if inputs == "1":

    backtracking_search(sudokucsp)

elif inputs == "2":

    backtracking_search(sudokucsp, mrv_degree, lcv, mac)

else:

    print("\nsystem exit!")
    sys.exit(0)


