"""
6x6 Grid Solver with C1 and C5 Constraints
- Fixed Seed: Cell (1,1) = 1
- C1 (Orthogonal): No orthogonally adjacent cells with consecutive numbers
- C5 (Rook Constraint): {1, 12, 24, 36} cannot share rows or columns
"""
 
def is_valid_placement(grid, row, col, num, size=6):
    """Check if placing num at (row, col) is valid."""
    # Check orthogonal adjacency constraint (C1)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < size and 0 <= nc < size and grid[nr][nc] != 0:
            neighbor = grid[nr][nc]
            if abs(neighbor - num) == 1:
                return False
    # Check rook constraint (C5) for special numbers
    special_nums = {1, 12, 24, 36}
    if num in special_nums:
        # Check row for other special numbers
        for c in range(size):
            if c != col and grid[row][c] in special_nums:
                return False
        # Check column for other special numbers
        for r in range(size):
            if r != row and grid[r][col] in special_nums:
                return False
    return True
 
def is_number_used(grid, num, size=6):
    """Check if a number is already used in the grid."""
    for row in grid:
        if num in row:
            return True
    return False
 
def solve_grid(grid, pos=1, size=6):
    """Backtracking solver starting from position 1 (since pos 0 is fixed to 1)."""
    if pos == size * size:
        return True
    row, col = pos // size, pos % size
    # Try numbers 2-36 (1 is already placed at position 0)
    for num in range(2, size * size + 1):
        # Check if number is already used
        if is_number_used(grid, num, size):
            continue
        if is_valid_placement(grid, row, col, num, size):
            grid[row][col] = num
            if solve_grid(grid, pos + 1, size):
                return True
            grid[row][col] = 0
    return False
 
def format_solution(grid):
    """Format grid as comma-separated string."""
    result = []
    for row in grid:
        result.extend(row)
    return ','.join(map(str, result))
 
def print_grid(grid):
    """Pretty print the grid."""
    for row in grid:
        print(' '.join(f'{num:2d}' for num in row))
 
def verify_solution(grid, size=6):
    """Verify that the solution satisfies all constraints."""
    print("\n=== Verification ===")
    # Check fixed seed
    if grid[0][0] != 1:
        print(f" Fixed seed failed: grid[0][0] = {grid[0][0]}, expected 1")
        return False
    print(f"✓ Fixed seed: grid[0][0] = 1")
    # Check all numbers 1-36 are used exactly once
    all_nums = []
    for row in grid:
        all_nums.extend(row)
    if sorted(all_nums) != list(range(1, size * size + 1)):
        print(" Not all numbers 1-36 used exactly once")
        return False
    print(f"✓ All numbers 1-36 used exactly once")
    # Check C1 constraint
    c1_violations = 0
    for r in range(size):
        for c in range(size):
            val = grid[r][c]
            # Check right neighbor
            if c < size - 1 and abs(grid[r][c+1] - val) == 1:
                c1_violations += 1
            # Check bottom neighbor
            if r < size - 1 and abs(grid[r+1][c] - val) == 1:
                c1_violations += 1
    if c1_violations > 0:
        print(f" C1 constraint violated {c1_violations} times")
        return False
    print(f"✓ C1 constraint satisfied (no orthogonally adjacent consecutive numbers)")
    # Check C5 constraint
    special_nums = {1, 12, 24, 36}
    special_positions = {}
    for r in range(size):
        for c in range(size):
            if grid[r][c] in special_nums:
                special_positions[grid[r][c]] = (r, c)
    c5_violations = 0
    for num1 in special_nums:
        for num2 in special_nums:
            if num1 < num2 and num1 in special_positions and num2 in special_positions:
                r1, c1 = special_positions[num1]
                r2, c2 = special_positions[num2]
                if r1 == r2 or c1 == c2:
                    print(f" C5 violation: {num1} at ({r1},{c1}) and {num2} at ({r2},{c2})")
                    c5_violations += 1
    if c5_violations > 0:
        return False
    print(f"✓ C5 constraint satisfied ({special_nums} rook constraint)")
    print(f"  Special number positions: {special_positions}")
    return True
 
def main():
    size = 6
    grid = [[0] * size for _ in range(size)]
    # Fixed seed: top-left cell = 1
    grid[0][0] = 1
    print("Solving 6x6 grid with constraints...")
    print("- Fixed: Cell (1,1) = 1")
    print("- C1: No orthogonally adjacent consecutive numbers")
    print("- C5: {1, 12, 24, 36} rook constraint (no two in same row/column)")
    print()
    if solve_grid(grid):
        print("✓ Solution found!\n")
        print_grid(grid)
        # Verify the solution
        if verify_solution(grid, size):
            print(format_solution(grid))
        else:
            print("\n Solution verification failed!")
    else:
        print("No solution found.")
 
if __name__ == "__main__":
    main()