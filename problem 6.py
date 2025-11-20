N = 6

rooks = {1, 12, 24, 36}

orthogonal_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
 
def is_valid(grid, r, c, val, row_rooks, col_rooks):

    # Check rook constraint

    if val in rooks:

        if row_rooks[r] or col_rooks[c]:

            return False

    # Check orthogonal adjacency for consecutive numbers

    for dr, dc in orthogonal_dirs:

        nr, nc = r + dr, c + dc

        if 0 <= nr < N and 0 <= nc < N:

            neighbor = grid[nr][nc]

            if neighbor is not None and abs(neighbor - val) == 1:

                return False

    return True
 
def backtrack(grid, used, row_rooks, col_rooks, pos=0):

    if pos == N * N:

        return True

    r, c = divmod(pos, N)

    if r == 0 and c == 0:

        return backtrack(grid, used, row_rooks, col_rooks, pos + 1)
 
    for val in range(1, N * N + 1):

        if not used[val]:

            if is_valid(grid, r, c, val, row_rooks, col_rooks):

                grid[r][c] = val

                used[val] = True

                if val in rooks:

                    row_rooks[r] = True

                    col_rooks[c] = True
 
                if backtrack(grid, used, row_rooks, col_rooks, pos + 1):

                    return True
 
                # Undo assignment

                grid[r][c] = None

                used[val] = False

                if val in rooks:

                    row_rooks[r] = False

                    col_rooks[c] = False

    return False
 
def validate_solution(grid):

    # Validate grid dimensions and unique numbers

    all_values = [grid[r][c] for r in range(N) for c in range(N)]

    if sorted(all_values) != list(range(1, N * N + 1)):

        return False, "Grid numbers invalid or duplicated"
 
    # Check top-left fixed seed

    if grid[0][0] != 1:

        return False, "Top-left cell is not 1"
 
    # Validate rook constraint: no same rook numbers share row or column

    rook_positions = {rnum: [] for rnum in rooks}

    for r in range(N):

        for c in range(N):

            val = grid[r][c]

            if val in rooks:

                rook_positions[val].append((r, c))
 
    # Check that rook numbers are separated by row and column

    for rook1 in rooks:

        for rook2 in rooks:

            if rook1 >= rook2:

                continue

            for (r1, c1) in rook_positions[rook1]:

                for (r2, c2) in rook_positions[rook2]:

                    if r1 == r2 or c1 == c2:

                        return False, f"Rook numbers {rook1} and {rook2} share row or column"
 
    # Validate no orthogonal adjacent cells have consecutive numbers

    for r in range(N):

        for c in range(N):

            val = grid[r][c]

            for dr, dc in orthogonal_dirs:

                nr, nc = r + dr, c + dc

                if 0 <= nr < N and 0 <= nc < N:

                    nval = grid[nr][nc]

                    if abs(val - nval) == 1:

                        return False, f"Consecutive numbers {val} and {nval} adjacent at {(r,c)} and {(nr,nc)}"

    return True, "Valid solution"
 
def main():

    grid = [[None] * N for _ in range(N)]

    grid[0][0] = 1
 
    used = [False] * (N * N + 1)

    used[1] = True
 
    row_rooks = [False] * N

    col_rooks = [False] * N

    row_rooks[0] = True

    col_rooks[0] = True
 
    if backtrack(grid, used, row_rooks, col_rooks):

        valid, message = validate_solution(grid)

        if valid:

            result = ",".join(str(grid[r][c]) for r in range(N) for c in range(N))

            print("Solution found:\n", result)

        else:

            print("Solution invalid:", message)

    else:

        print("No solution found")
 
if __name__ == "__main__":

    main()

 