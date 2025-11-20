import itertools
from typing import List, Set, Tuple

def is_valid_grid(grid: List[List[int]]) -> bool:
    """Check if grid satisfies all constraints"""
    
    # C1: Orthogonal constraint - no consecutive numbers adjacent
    for r in range(5):
        for c in range(5):
            val = grid[r][c]
            # Check up
            if r > 0 and abs(grid[r-1][c] - val) == 1:
                return False
            # Check down
            if r < 4 and abs(grid[r+1][c] - val) == 1:
                return False
            # Check left
            if c > 0 and abs(grid[r][c-1] - val) == 1:
                return False
            # Check right
            if c < 4 and abs(grid[r][c+1] - val) == 1:
                return False
    
    # C2: Diagonal constraint - no difference of 2 diagonally adjacent
    for r in range(5):
        for c in range(5):
            val = grid[r][c]
            # Check all 4 diagonal neighbors
            if r > 0 and c > 0 and abs(grid[r-1][c-1] - val) == 2:
                return False
            if r > 0 and c < 4 and abs(grid[r-1][c+1] - val) == 2:
                return False
            if r < 4 and c > 0 and abs(grid[r+1][c-1] - val) == 2:
                return False
            if r < 4 and c < 4 and abs(grid[r+1][c+1] - val) == 2:
                return False
    
    # C3: Prime cells sum must be even
    prime_cells = [(0,1), (0,3), (1,0), (1,2), (2,1), (2,3), (3,0), (3,2), (4,1), (4,3)]
    prime_sum = sum(grid[r][c] for r, c in prime_cells)
    if prime_sum % 2 != 0:
        return False
    
    return True

def solve_with_backtracking():
    """Use backtracking to find a valid solution"""
    grid = [[0]*5 for _ in range(5)]
    used = [False] * 26  # 1-25
    
    # Fix center cell
    grid[2][2] = 13
    used[13] = True
    
    def can_place(r, c, val):
        """Check if we can place val at position (r,c)"""
        # C1: Check orthogonal neighbors
        if r > 0 and grid[r-1][c] != 0 and abs(grid[r-1][c] - val) == 1:
            return False
        if c > 0 and grid[r][c-1] != 0 and abs(grid[r][c-1] - val) == 1:
            return False
        if r < 4 and grid[r+1][c] != 0 and abs(grid[r+1][c] - val) == 1:
            return False
        if c < 4 and grid[r][c+1] != 0 and abs(grid[r][c+1] - val) == 1:
            return False
        
        # C2: Check diagonal neighbors
        if r > 0 and c > 0 and grid[r-1][c-1] != 0 and abs(grid[r-1][c-1] - val) == 2:
            return False
        if r > 0 and c < 4 and grid[r-1][c+1] != 0 and abs(grid[r-1][c+1] - val) == 2:
            return False
        if r < 4 and c > 0 and grid[r+1][c-1] != 0 and abs(grid[r+1][c-1] - val) == 2:
            return False
        if r < 4 and c < 4 and grid[r+1][c+1] != 0 and abs(grid[r+1][c+1] - val) == 2:
            return False
        
        return True
    
    def backtrack(pos):
        if pos == 25:
            # Check C3: prime cells sum even
            prime_cells = [(0,1), (0,3), (1,0), (1,2), (2,1), (2,3), (3,0), (3,2), (4,1), (4,3)]
            prime_sum = sum(grid[r][c] for r, c in prime_cells)
            return prime_sum % 2 == 0
        
        r, c = pos // 5, pos % 5
        
        # Skip center cell (already set)
        if r == 2 and c == 2:
            return backtrack(pos + 1)
        
        # Try each unused value
        for val in range(1, 26):
            if not used[val] and can_place(r, c, val):
                grid[r][c] = val
                used[val] = True
                
                if backtrack(pos + 1):
                    return True
                
                grid[r][c] = 0
                used[val] = False
        
        return False
    
    if backtrack(0):
        return grid
    return None

print("Solving 5x5 grid puzzle...")
print("This may take a while due to the strict constraints...")

solution = solve_with_backtracking()

if solution:
    print("\nFound valid solution:")
    for row in solution:
        print(row)
    
    # Format as comma-separated string
    result = []
    for row in solution:
        result.extend(row)
    print("\nSubmission format:")
    print(','.join(map(str, result)))
    
    # Verify constraints
    print("\nVerifying constraints:")
    print(f"Center cell (3,3) = {solution[2][2]} (should be 13)")
    
    prime_cells = [(0,1), (0,3), (1,0), (1,2), (2,1), (2,3), (3,0), (3,2), (4,1), (4,3)]
    prime_sum = sum(solution[r][c] for r, c in prime_cells)
    print(f"Prime cells sum = {prime_sum} (even: {prime_sum % 2 == 0})")
else:
    print("No solution found!")
