# Count number of valid 5x5 grids using only C1 (orthogonal: no N next to N±1)
 
from itertools import permutations
 
# adjacency directions (orthogonal only)
dirs = [(-1,0),(1,0),(0,-1),(0,1)]
 
def build_adj_list():
    adj = {}
    for r in range(5):
        for c in range(5):
            neighbors = []
            for dr, dc in dirs:
                rr, cc = r + dr, c + dc
                if 0 <= rr < 5 and 0 <= cc < 5:
                    neighbors.append((rr, cc))
            adj[(r, c)] = neighbors
    return adj
 
adj = build_adj_list()
 
# check C1 on-the-fly
def valid_place(grid, r, c, val):
    for rr, cc in adj[(r, c)]:
        if grid[rr][cc] is not None:
            other = grid[rr][cc]
            if abs(other - val) == 1:   # C1 violation
                return False
    return True
 
grid = [[None]*5 for _ in range(5)]
used = set()
count = 0
 
def solve(i=0):
    global count
 
    if i == 25:
        count += 1
        return
 
    r, c = divmod(i, 5)
 
    for val in range(1, 26):
        if val in used:
            continue
 
        if valid_place(grid, r, c, val):
            grid[r][c] = val
            used.add(val)
 
            solve(i+1)
 
            used.remove(val)
            grid[r][c] = None
 
# run the solver
solve()
 
print("Total valid solutions (C1 only):", count)