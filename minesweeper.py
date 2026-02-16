import random
#import file "this for if you want to import something from another file"

def place_mines(num_mines, rows=10, cols=10):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()
    while len(mine_positions) < num_mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        if (r, c) not in mine_positions:
            mine_positions.add((r, c))
            board[r][c] = -1  # -1 represents a mine
            # Fill in numbers for non-mine cells
    
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == -1:
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == -1:
                        count += 1
            board[r][c] = count
    return board

mines_board = place_mines(20)  # Places 20 mines randomly

def surrounding_mines(board, row, col):
    rows = len(board)
    cols = len(board[0])
    mine_count = 0
    for r in range(max(0, row - 1), min(rows, row + 2)):
        for c in range(max(0, col - 1), min(cols, col + 2)):
            if board[r][c] == -1:
                mine_count += 1
    return mine_count

# For testing, we will fill in the counts for non-mine cells
for i in range(len(mines_board)):
    for j in range(len(mines_board[0])):
        if mines_board[i][j] != -1:
            mines_board[i][j] = surrounding_mines(mines_board, i, j)

for row in mines_board:
    print(row)

