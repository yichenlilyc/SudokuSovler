# Sudoku Solver

# Instruction

This is a solution of Sudoku based on the general [CSP Solver](http://yichenliclaire.com/2020/01/17/CSP-Solver/).

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb058rvc39j311603edid.jpg)

Running the program, the first thing is to input the sudoku file that needs to be solved. After inputting the filename, if the file is existing, the program will show you the input sudoku problem as a matrix.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb059srhtlj30x70u0b29.jpg)

Also, vertex, neighbor and domains.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb05avmbx3j31o4052n62.jpg)

And Initial state.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb05bsgdj6j30u0113kh8.jpg)

Then the program will do AC-3 to check this problem, after this, you could input number to choose different methods to solve the problem.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb05cny442j312c09yaex.jpg)

After this, the program will tell you the result, if this problem has a solution.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb05eaaq05j314f0u0ani.jpg)

If the input problem doesn’t have a solution, the program will tell you “No such assignment is possible”.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb05f41ji1j30pm04ctae.jpg)

# The detailed description of the application

Our problem could not only solve the 9*9 sudoku problem but also the n*n sudoku problem(n must be a number squared). The vertex of our program is the x-axis and y-axis in the sudoku map. The constraint of our program follows the rules of sudoku problem.

Each row, column, and √n * √n grids can contain each number (in 9*9 sudoku problem, 1 to 9, in n*n problem, 1 to n) exactly once.
 The domain is different based on the different problem, in n*n sudoku problem, the domain is 1 to n.

# Adaption of CSP solver

The sudoku extends the class of the CSP with parameters variables, values, neighbors and constraints. The constraints has been changed in the instance of sudoku part, and compared with part 1, the deadline constraint is canceled. The detailed adaption of algorithm and heuristic functions in part 1 is described in the following paragraph.

## AC3

AC3 algorithm is firstly used before backtracking search to reduce the domains of each variable. For any two variables that have mutual constraints (any two squares in the same row, or the same column, or in the same large square in Sudoku), the AC3 is used to reduce the domain of each grid. Reduce subsequent space and time consumption. In the first round of assignment, the known squares in the title are filled in. At this time, using AC3 algorithm to judge the arc consistency can greatly reduce the domain of some squares. For some simpler (more known values) Sudoku, you can get the solution directly without continuing the subsequent search. AC3 is also used in backtracking, maintaining the arc consistency every time a value was assigned.

```
Function AC-3(csp) returns false if an inconsistency is found and true otherwise 
	Inputs: csp
	Local variables: queue(initially all the arcs in constraints)
	
	While queue is not empty do 
		(Xi,Xj)=queue.pop()
	If Revise(csp,Xi,Xj) then
		If size of Di=0 then 
			return false
		For each Xk in Xi.Neighbors-{Xj} do
			Add(Xk,Xi)to queue
	Return true
	
Function Revise(csp,Xi,Xj) returns true iff revise the domain of Xi 
	Revise=false
	For each x in Di do
		If no value y in Dj allows(x,y) to satisfy the constraint between Xi and Xj then
			Delete x from Di
			Revised=true
			return Revised
```

## Backtracking

Backtracking is used to search assignments for each empty grid. In the implementation of Sudoku, the first round of assignment is to fill the know squares, so there is no need to do backtracking for the assignment. For the problem that cannot be fully solved by AC3, backtracking is used to find the assignment for the rest squares. In this approach, minimum-remaining value heuristic is used to choose the variable. Least constraint value heuristic is used to choose the value that will be assigned to the variable. And for each assignment, AC3 is used to inference the availability.

```
Function Backtracking_search(csp) returns a solution or failure Function 			
	Backtrack(assignment):
		If assignment is complete return assignment 
			Var=select_unassigned_variable(assignment, csp) (using MRV)
		For values in Order_domain_values(var,assignment,csp) (using LCV)
			If value is consistent with assignment then 
				Csp.assign(var, value, assignment)
				Remove value from csp.current_domain
				If inference !=failure(using AC3 as inference) 
					Result=Backtrack(assignment)
				If result is not none:
					Return result
		Return none
```

## Minimum remaining value heuristic

In Sudoku, after AC3, the domains of some variables are reduced. Then assign value to variable that has least minimum remaining values first. The heuristic is used in backtracking to choose the variable that first to be assigned.

```
Function mrv_degree(assignment, csp):
	Dictionary[csp.variable]=variable.current_domain 
	Order=Sort Dictionary by the quantities of items
	While quantities of variables: 
		Variable=the first variable in order
	If there are two variables has the same remain value 
		Variable= the length is the largest
		Return variable
```

# Result

We test many problems, includes 9*9 sudoku, 16 * 16 sudoku and 25* 25 sudoku. Our program passed all 9*9 and 16*16 sudoku. When solving 25*25 sudoku, our program will spend a long time, and because of space is not enough, so we can’t get the correct answer on our computer.

Notice that in p4, our program could directly reach the goal by only doing AC3, it will save a lot of time.
 When solving 9*9 and 16*16 sudoku problem, our program performs very well, however, if solving more complicated sudoku problem, such as 25*25, our program will have some efficiency problem and memory out of space problem so may not get the correct answer in our computer.

P1.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb068e2qqpj313e0kkwzq.jpg)

P2.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb069ahi3cj31760lke5j.jpg)

P3.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb06at94fcj31760n0ngb.jpg)

P4.

![](https://tva1.sinaimg.cn/large/006tNbRwgy1gb06bl75gnj31ao0jk18v.jpg)

