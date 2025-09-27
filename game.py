import random
from typing import List, Dict, Any, Tuple, Optional

MINE = -1

def place_mines(num_mines: int, rows: int = 10, cols: int = 10, x: Optional[int] = None, y: Optional[int] = None) -> List[List[int]]:
    """Create a new board with mines (-1) and neighbor counts (0–8)."""
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

    # Place mines
    while len(mine_positions) < num_mines:
        r, c = random.randrange(rows), random.randrange(cols)
        if (r, c) not in mine_positions:
            mine_positions.add((r, c))
            board[r][c] = MINE
    # remove mines from spot user clicked and adjacent squares
    print(x,y)
    if x and y:
        for offset_x in [-1, 0, 1]:
            for offset_y in [-1, 0, 1]:
                board[x + offset_x][y + offset_y] = None

    # Fill counts for non-mine cells
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != MINE:
                board[r][c] = surrounding_mines(board, r, c)

    return board

def surrounding_mines(board, row, col) -> int:
    rows, cols = len(board), len(board[0])
    count = 0
    for rr in range(max(0, row - 1), min(rows, row + 2)):
        for cc in range(max(0, col - 1), min(cols, col + 2)):
            if (rr, cc) != (row, col) and board[rr][cc] == MINE:
                count += 1
    return count

def create_game(board: List[List[int]]) -> Dict[str, Any]:
    """Wrap a board into a game state dict."""
    size = len(board)
    mine_count = sum(cell == MINE for row in board for cell in row)
    grid = [
        [
            {"mine": board[r][c] == MINE,
             "revealed": False,
             "flagged": False,
             "srr": 0 if board[r][c] == MINE else board[r][c]}
            for c in range(size)
        ]
        for r in range(size)
    ]
    return {
        "size": size,
        "mine_count": mine_count,
        "grid": grid,
        "flags_left": mine_count,
        "playing": True,
        "won": False,
        "GameState": "Menu", # can be Menu, ThemeSelector, MineSelector, Single, AiEasy, AiMedium, AiHard
        "theme": "Themes/OG/", # can be Themes/Drawn/, Themes/OG/, Themes/Dark/, Themes/Light/
        "ai_difficulty": "easy", # hard-coded AI difficulty
        "current_turn": "human", # human goes first, then alternates with AI
    }

def neighbors(state, r, c):
    size = state["size"]
    for rr in range(max(0, r - 1), min(size, r + 2)):
        for cc in range(max(0, c - 1), min(size, c + 2)):
            if (rr, cc) != (r, c):
                yield rr, cc

def reveal(state, r, c) -> Tuple[bool, str]:
    """Reveal a cell. Returns (finished, message)."""
    if not state["playing"]:
        return True, "Game finished."
    cell = state["grid"][r][c]
    if cell["flagged"]:
        return False, "Cell flagged."
    if cell["revealed"]:
        return False, "Already revealed."
    cell["revealed"] = True
    if cell["mine"]:
        state["playing"] = False
        return True, "Mine hit!"
    if cell["srr"] == 0:
        flood_fill(state, r, c)
    if check_win(state):
        state["playing"] = False
        state["won"] = True
        return True, "You won!"
    
    # Switch turns if game is still playing
    if state["playing"] and state["current_turn"] == "human":
        state["current_turn"] = "ai"
    
    return False, "Revealed."

def flood_fill(state, r, c):
    stack = [(r, c)]
    visited = set(stack)
    while stack:
        cr, cc = stack.pop()
        for nr, nc in neighbors(state, cr, cc):
            cell = state["grid"][nr][nc]
            if cell["revealed"] or cell["flagged"] or cell["mine"]:
                continue
            cell["revealed"] = True
            if cell["srr"] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append((nr, nc))

def toggle_flag(state, r, c) -> str:
    if not state["playing"]:
        return "Game over."
    cell = state["grid"][r][c]
    if cell["revealed"]:
        return "Can't flag revealed cell."
    if cell["flagged"]:
        cell["flagged"] = False
        state["flags_left"] += 1
        return "Flag removed."
    if state["flags_left"] == 0:
        return "No flags left."
    cell["flagged"] = True
    state["flags_left"] -= 1
    return "Flag placed."

def check_win(state) -> bool:
    safe_cells = state["size"] * state["size"] - state["mine_count"]
    revealed = sum(1 for row in state["grid"] for c in row if c["revealed"] and not c["mine"])
    return revealed == safe_cells

def ai_make_move(state) -> Tuple[bool, str]:
    
    if not state["playing"] or state["current_turn"] != "ai":
        return False, "Not AI's turn or game finished."
    
    if state["ai_difficulty"] == "easy":
        return ai_easy_move(state)
    
    return False, "Unknown AI difficulty."

def ai_easy_move(state) -> Tuple[bool, str]:
    
    # Get all valid cells (not revealed, not flagged)
    valid_cells = []
    for r in range(state["size"]):
        for c in range(state["size"]):
            cell = state["grid"][r][c]
            if not cell["revealed"] and not cell["flagged"]:
                valid_cells.append((r, c))
    
    if not valid_cells:
        return False, "No valid moves for AI."
    
    # Pick a random valid cell
    r, c = random.choice(valid_cells)
    
    # Make the move
    finished, message = reveal(state, r, c)
    
    # Switch turn back to human after AI move
    if state["playing"]:  # Only switch if game is still ongoing
        state["current_turn"] = "human"
    
    return finished, f"AI revealed ({r}, {c}): {message}"
