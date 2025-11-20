4 one -----
# Solves the 5x5 constraint puzzle with C1, C2, C3, and C4 (median = 14)
 
# Prime-indexed cells from problem statement
prime_cells = {
    (1,2),(1,4),(2,1),(2,3),(3,2),
    (3,4),(4,1),(4,3),(5,2),(5,4)
}
prime_cells = {(r-1, c-1) for r, c in prime_cells}
 
# Directions
orth = [(-1,0),(1,0),(0,-1),(0,1)]
diag = [(-1,-1),(-1,1),(1,-1),(1,1)]
 
grid = [[None]*5 for _ in range(5)]
used = set()
 
# Fixed seed
grid[2][2] = 13
used.add(13)
 
# Check constraints
def valid(r, c, val):
    # C1 – orthogonal consecutive forbidden
    for dr, dc in orth:
        rr, cc = r + dr, c + dc
        if 0 <= rr < 5 and 0 <= cc < 5:
            if grid[rr][cc] is not None:
                if abs(grid[rr][cc] - val) == 1:
                    return False
 
    # C2 – diagonal difference 2 forbidden
    for dr, dc in diag:
        rr, cc = r + dr, c + dc
        if 0 <= rr < 5 and 0 <= cc < 5:
            if grid[rr][cc] is not None:
                if abs(grid[rr][cc] - val) == 2:
                    return False
 
    return True
 
def median_ok():
    row = grid[0]
    if None in row:
        return True
    return sorted(row)[2] == 14  # C4
 
def prime_sum_ok():
    total = sum(grid[r][c] for r, c in prime_cells)
    return total % 2 == 0  # C3
 
# Backtracking
def solve(i=0):
    if i == 25:
        return prime_sum_ok() and median_ok()
 
    r, c = divmod(i, 5)
 
    # skip fixed center
    if (r, c) == (2, 2):
        return solve(i + 1)
 
    for val in range(1, 26):
        if val in used:
            continue
 
        if not valid(r, c, val):
            continue
 
        grid[r][c] = val
        used.add(val)
 
        if r == 0 and all(x is not None for x in grid[0]):
            if not median_ok():
                grid[r][c] = None
                used.remove(val)
                continue
 
        if solve(i + 1):
            return True
 
        grid[r][c] = None
        used.remove(val)
 
    return False
 
solve()
 
# Print full grid
for row in grid:
    print(row)
 
# Required output: value at Grid(5,5)
print("\nAnswer (Grid 5,5):", grid[4][4])