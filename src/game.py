"""Minesweeper game logic.

Funcs:
    create_game(board) -> state dict
    reveal(state, r, c) -> (finished: bool, message: str)
    toggle_flag(state, r, c) -> message
    text_render(state, reveal_mines=False) -> string representation
    cell_state(state, r, c) -> copy of one cell dict

State dict keys: size, mine_count, grid, flags_left, playing, won
Cell dict: mine (bool), revealed (bool), flagged (bool), srr (int)

Iterative flood fill instead of recursion.
"""

from typing import List, Tuple, Dict, Any

MINE_VALUE = -1


def create_game(board: List[List[int]]) -> Dict[str, Any]:
    """Wrap existing board into game state.
        board: Square 2D list.
        Each non-mine cell holds its surrounding mine count (0-8) stored in field 'srr'.
    """
    size = len(board)
    mine_count = 0
    grid: List[List[Dict[str, Any]]] = []
    for r in range(size):
        row_cells: List[Dict[str, Any]] = []
        for c in range(size):
            val = board[r][c]
            if val == MINE_VALUE:
                mine_count += 1
            elif not (0 <= val <= 8):  # square grid, max 8 neighbors.
                raise ValueError("Non-mine cells must have surrounding mine count 0-8.")
            row_cells.append({
                'mine': val == MINE_VALUE,
                'revealed': False,
                'flagged': False,
                'srr': 0 if val == MINE_VALUE else val,
            })
        grid.append(row_cells)

    return {
        'size': size,
        'mine_count': mine_count,
        'grid': grid,
        'flags_left': mine_count,
        'playing': True,
        'won': False,
    }

def _neighbors(state: Dict[str, Any], r: int, c: int):
    size = state['size']
    for rr in range(max(0, r - 1), min(size, r + 2)):
        for cc in range(max(0, c - 1), min(size, c + 2)):
            if (rr, cc) != (r, c):
                yield rr, cc


def reveal(state: Dict[str, Any], r: int, c: int) -> Tuple[bool, str]:
    if not state['playing']:
        return True, "Game already finished."
    size = state['size']
    if not (0 <= r < size and 0 <= c < size):
        return False, "Out of bounds."
    cell = state['grid'][r][c]
    if cell['flagged']:
        return False, "Cell is flagged."
    if cell['revealed']:
        return False, "Already revealed."
    cell['revealed'] = True
    if cell['mine']:
        state['playing'] = False
        return True, "Mine hit"
    if cell['srr'] == 0:
        _flood_fill(state, r, c)
    if _check_win(state):
        state['playing'] = False
        state['won'] = True
        return True, "You won"
    return False, "Revealed."


def _flood_fill(state: Dict[str, Any], r: int, c: int):
    stack = [(r, c)]
    visited = set(stack)
    while stack:
        cr, cc = stack.pop()
        for nr, nc in _neighbors(state, cr, cc):
            cell = state['grid'][nr][nc]
            if cell['revealed'] or cell['flagged'] or cell['mine']:
                continue
            cell['revealed'] = True
            if cell['srr'] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append((nr, nc))


def toggle_flag(state: Dict[str, Any], r: int, c: int) -> str:
    if not state['playing']:
        return "Game is over."
    if not (0 <= r < state['size'] and 0 <= c < state['size']):
        return "Out of bounds."
    cell = state['grid'][r][c]
    if cell['revealed']:
        return "Can't flag revealed cell."
    if cell['flagged']:
        cell['flagged'] = False
        state['flags_left'] += 1
        return "Flag removed."
    if state['flags_left'] == 0:
        return "No flags left."
    cell['flagged'] = True
    state['flags_left'] -= 1
    return "Flag placed."


def _check_win(state: Dict[str, Any]) -> bool:
    size = state['size']
    safe_cells = size * size - state['mine_count']
    revealed = sum(
        1 for row in state['grid'] for cell in row if cell['revealed'] and not cell['mine']
    )
    return revealed == safe_cells


def text_render(state: Dict[str, Any], reveal_mines: bool = False) -> str:
    size = state['size']
    lines: List[str] = []
    for r in range(size):
        parts = []
        for c in range(size):
            cell = state['grid'][r][c]
            if cell['revealed']:
                if cell['mine']:
                    parts.append('*')
                else:
                    parts.append(str(cell['srr']) if cell['srr'] > 0 else ' ')
            else:
                if cell['flagged']:
                    parts.append('F')
                elif reveal_mines and cell['mine']:
                    parts.append('*')
                else:
                    parts.append('#')
        lines.append(' '.join(parts))
    return '\n'.join(lines)


def cell_state(state: Dict[str, Any], r: int, c: int):
    return dict(state['grid'][r][c])

# Example usage:
'''
state = create_game(board)
print(text_render(state))
# Reveal a safe zero or number
finished, msg = reveal(state, 0, 4)  # top-right corner (0)
print(\"\\nReveal (0,4):\", msg)
print(text_render(state))

# Flag a suspected mine
print(\"\\nFlag (0,0):\", toggle_flag(state, 0, 0))
print(text_render(state))

# Try to reveal a flagged cell (should be blocked)
finished, msg = reveal(state, 0, 0)
print(\"Reveal flagged (0,0):\", msg)

# Unflag then reveal the mine to lose
print(\"Unflag (0,0):\", toggle_flag(state, 0, 0))
finished, msg = reveal(state, 0, 0)
print(\"Reveal mine (0,0):\", msg)
print(text_render(state, reveal_mines=True))  # Show all mines after loss
'''
