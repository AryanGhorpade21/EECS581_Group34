import random
from typing import List, Dict, Any, Tuple, Optional

MINE = -1

# Helper to skip tile if it's too close to an existing mine
def too_close(r, c, mine_positions, spread):
    for mr, mc in mine_positions:
        if abs(r -mr) <= spread and abs(c - mc) <= spread:
            return True
    return False 

def place_mines(num_mines: int, rows: int = 10, cols: int = 10, x: Optional[int] = None, y: Optional[int] = None, spread: int = 0) -> List[List[int]]:
    """Create a new board with mines (-1) and neighbor counts (0–8)."""
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

 
    forbidden = set() # squresnot allowed to have bombs
    if x is not None and y is not None:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    forbidden.add((nx, ny))

    # Place mines with repulsion logic 
    attempts = 0
    max_attempts = rows * cols * 10 # safeguard to avoid infinite loop
    while len(mine_positions) < num_mines and attempts < max_attempts:
        r, c = random.randrange(rows), random.randrange(cols)
        attempts += 1

        if (r, c) in mine_positions or (r, c) in forbidden:
            continue
        if too_close(r, c, mine_positions, spread):
            continue

        mine_positions.add((r, c))
        board[r][c] = MINE

    if len(mine_positions) < num_mines:
        print(f"Warning: only placed {len(mine_positions)} mines (spread too high).")

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
        "NumMines": 10,
        "grid": grid,
        "flags_left": mine_count,
        "playing": True,
        "won": False,
        "GameState": "Menu", # can be Menu, ThemeSelector, MineSelector, Single, AiEasy, AiMedium, AiHard
        "theme": "Themes/OG/", # can be Themes/Drawn/, Themes/OG/, Themes/Dark/, Themes/Light/
        "ai_difficulty": "none", # AI difficulty - can be "none", "easy", "medium", or "hard"
        "ai_enabled": False, # Whether AI is enabled or playing solo
        "current_turn": "human", # human goes first, then alternates with AI (if enabled)
        "music_muted": False, #control bg music on or off
        "density": 1 # tracks how spread out the mines are from each other - 0 = high density (clustered), 1 = spread out
    }

def neighbors(state, r, c):
    size = state["size"]
    for rr in range(max(0, r - 1), min(size, r + 2)):
        for cc in range(max(0, c - 1), min(size, c + 2)):
            if (rr, cc) != (r, c):
                yield rr, cc

def reveal(state, r, c) -> Tuple[bool, str]:
    """Reveal a cell. Returns (finished, message)."""
    state["ai_hit_bomb"] = False
    if not state["playing"]:
        return True, "Game finished."
    cell = state["grid"][r][c]
    if cell["flagged"]:
        return False, "Cell flagged."
    if cell["revealed"]:
        return False, "Already revealed."
    cell["revealed"] = True
    
    # Check for mine hit first (Game Over)
    if cell["mine"]:
        state["playing"] = False
        if state["current_turn"] == "ai":
            state["ai_hit_bomb"] = True
        return True, "Mine hit!"
        
    # Perform flood fill for safe empty cells
    if cell["srr"] == 0:
        flood_fill(state, r, c) # <--- Flood fill completes the move

    # Now, check for a win after the cell (or multiple cells) has been revealed
    if check_win(state): 
        state["playing"] = False
        state["won"] = True
        return True, "You won!"
    
    # Switch turns if game is still playing and AI is enabled
    if state["playing"] and state.get("ai_enabled", True) and state["current_turn"] == "human":
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
    elif state["ai_difficulty"] == "medium":
        return ai_medium_move(state)
    elif state["ai_difficulty"] == "hard":
        return ai_hard_move(state)
    
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
    if state["playing"]: 
        state["current_turn"] = "human"
    
    return finished, f"AI revealed ({r}, {c}): {message}"

def ai_medium_move(state) -> Tuple[bool, str]:
    
    flags_placed = 0
    max_flags_per_turn = 3
    actions_taken = []
    
    # Rule 1: Flag hidden neighbors when count matches (up to 3 flags per turn)
    while flags_placed < max_flags_per_turn:
        flag_placed_this_iteration = False
        
        for r in range(state["size"]):
            for c in range(state["size"]):
                cell = state["grid"][r][c]
                if cell["revealed"] and cell["srr"] > 0:
                    # Get neighbors
                    hidden_neighbors = []
                    flagged_neighbors = []
                    
                    for nr, nc in neighbors(state, r, c):
                        neighbor = state["grid"][nr][nc]
                        if not neighbor["revealed"]:
                            if neighbor["flagged"]:
                                flagged_neighbors.append((nr, nc))
                            else:
                                hidden_neighbors.append((nr, nc))
                    
                    # If hidden neighbors count equals cell's number, flag all hidden neighbors
                    if len(hidden_neighbors) == cell["srr"]:
                        # Flag the first hidden neighbor
                        fr, fc = hidden_neighbors[0]
                        toggle_flag(state, fr, fc)
                        flags_placed += 1
                        actions_taken.append(f"flagged ({fr}, {fc})")
                        flag_placed_this_iteration = True
                        break
            
            if flag_placed_this_iteration:
                break
        
        # If no flag was placed this iteration, break out of the flagging loop
        if not flag_placed_this_iteration:
            break
    
    # Rule 2: Open safe neighbors when flags match count
    for r in range(state["size"]):
        for c in range(state["size"]):
            cell = state["grid"][r][c]
            if cell["revealed"] and cell["srr"] > 0:
                # Get neighbors
                hidden_neighbors = []
                flagged_neighbors = []
                
                for nr, nc in neighbors(state, r, c):
                    neighbor = state["grid"][nr][nc]
                    if not neighbor["revealed"]:
                        if neighbor["flagged"]:
                            flagged_neighbors.append((nr, nc))
                        else:
                            hidden_neighbors.append((nr, nc))
                
                # Rule 2: If flagged neighbors count equals cell number, open hidden neighbors
                if len(flagged_neighbors) == cell["srr"] and len(hidden_neighbors) > 0:
                    hr, hc = hidden_neighbors[0]
                    finished, message = reveal(state, hr, hc)
                    actions_taken.append(f"revealed ({hr}, {hc})")
                    
                    # Switch turn back to human after AI move
                    if state["playing"]:
                        state["current_turn"] = "human"
                    
                    action_summary = ", ".join(actions_taken)
                    return finished, f"AI (Medium) {action_summary}: {message}"
    
    # If we placed flags but couldn't find a safe reveal, must pick a random cell
    if flags_placed > 0:
        valid_cells = []
        for r in range(state["size"]):
            for c in range(state["size"]):
                cell = state["grid"][r][c]
                if not cell["revealed"] and not cell["flagged"]:
                    valid_cells.append((r, c))
        
        if valid_cells:
            r, c = random.choice(valid_cells)
            finished, message = reveal(state, r, c)
            actions_taken.append(f"revealed random ({r}, {c})")
            
            # Switch turn back to human after AI move
            if state["playing"]:
                state["current_turn"] = "human"
            
            action_summary = ", ".join(actions_taken)
            return finished, f"AI (Medium) {action_summary}: {message}"
    
    # Fallback: Pick a random hidden cell if no rules applied
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
    if state["playing"]:
        state["current_turn"] = "human"
    
    return finished, f"AI (Medium) revealed random cell ({r}, {c}): {message}"

def ai_hard_move(state) -> Tuple[bool, str]:
    # Get all valid cells that are safe (not revealed, not flagged, and not mines)
    safe_cells = []
    for r in range(state["size"]):
        for c in range(state["size"]):
            cell = state["grid"][r][c]
            if not cell["revealed"] and not cell["flagged"] and not cell["mine"]:
                safe_cells.append((r, c))
    
    if not safe_cells:
        # If no safe cells available, fall back to any valid cell 
        valid_cells = []
        for r in range(state["size"]):
            for c in range(state["size"]):
                cell = state["grid"][r][c]
                if not cell["revealed"] and not cell["flagged"]:
                    valid_cells.append((r, c))
        
        if not valid_cells:
            return False, "No valid moves for AI."
        
        r, c = random.choice(valid_cells)
    else:
        # Pick a random safe cell (AI "cheats" by knowing which cells are safe)
        r, c = random.choice(safe_cells)
    
    # Make the move
    finished, message = reveal(state, r, c)
    
    # Switch turn back to human after AI move
    if state["playing"]:  
        state["current_turn"] = "human"
    
    return finished, f"AI (Hard) revealed safe cell ({r}, {c}): {message}"
    
# Find a safe cell to reveal for the player
def safe_space_hint(state) -> Optional[Tuple[int, int]]:
    
    if "hints_left" not in state: # Default hints
        state["hints_left"] = 3  

    if state["hints_left"] <= 0: # No hints left, return none
        return None

    # Find all safe cells (not revealed, flagged, or mined)
    safe_cells = [
        (r, c)
        for r in range(state["size"])
        for c in range(state["size"])
        if not state["grid"][r][c]["revealed"]
        and not state["grid"][r][c]["flagged"]
        and not state["grid"][r][c]["mine"]
    ]

    if not safe_cells:
        return None
    
    # Pick random safe cell to reveal, and decrement hints available
    r, c = random.choice(safe_cells)
    reveal(state, r, c)
    state["hints_left"] -= 1
    return (r, c)

# Utilize the AI hard mode to solve the board
def solver_mode(state) -> List[Tuple[int, int]]:
    moves = []
    while state["playing"]:
        finished, message = ai_hard_move(state)
        moves.append((finished, message))
        if finished:
            break
    return moves
