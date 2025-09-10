"""game.py - Minesweeper game logic (no input/print here)

Provides: reveal(), toggle_flag(), remaining_flags(), status_line(), render().
Does:
    - Reveal cells (single, zero flood fill, chording re-click on numbers)
    - Track flags & revealed safe cells (flag cap == mine_count)
    - Detect win (all safe) / loss (mine hit)

Board setup must have: size, mine_count, _grid[List[List[Cell]]], _mines_placed,
    neighbors(r,c), parse_coord(token), render(reveal_mines)
Cell must have: is_mine, is_revealed, is_flagged, adjacent

Adjustments:
    - First-click safety area: _ensure_mines_placed()
    - Disable chording: remove _chord() call in reveal()
    - Different board size: change Board; this file reads board.size

Note: Wrong flags + chording can trigger an immediate loss.
"""

from enum import Enum
from typing import Tuple, List, Set
import random
from board import Board, Cell

class GameStatus(Enum):
    """Enumeration of overall game states."""
    PLAYING = "Playing"
    LOST = "Game Over"
    WON = "Victory"

class Game:
    def __init__(self, mine_count: int):
        """Initialize game with user-specified mine count (doesn't validate)."""
        self.board = Board(mine_count)
        self.status = GameStatus.PLAYING
        self.flags_placed = 0
        self._revealed_safe_cells = 0  # count revealed safe cells

    def _reveal_cell(self, r: int, c: int, flood: bool = True) -> bool:
        """Reveal one cell.
            flood: If True, perform flood fill from zero-adjacent cells.
            True if a mine was hit, else False.
        """
        cell: Cell = self.board._grid[r][c]
        if cell.is_revealed or cell.is_flagged:
            return False
        # mine placement: only on first actual reveal ensures safety region
        if not self.board._mines_placed:
            self._ensure_mines_placed(r, c)
        cell.is_revealed = True
        if cell.is_mine:
            return True
        self._revealed_safe_cells += 1
        if flood and cell.adjacent == 0:
            self._flood_fill(r, c)
        return False

    def _flood_fill(self, r: int, c: int):
        """Flood all nearby zero-adjacent cells and their numbered borders.
        """
        # stacking
        stack: List[Tuple[int, int]] = [(r, c)]
        visited: Set[Tuple[int, int]] = {(r, c)}
        while stack:
            cr, cc = stack.pop()
            for nr, nc in self.board.neighbors(cr, cc):
                ncell = self.board._grid[nr][nc]
                if ncell.is_revealed or ncell.is_flagged or ncell.is_mine:
                    continue
                ncell.is_revealed = True
                self._revealed_safe_cells += 1
                if ncell.adjacent == 0 and (nr, nc) not in visited:
                    stack.append((nr, nc))
                    visited.add((nr, nc))

    # --- Mine placement ---
    def _place_mines(self, safe_cells: Set[Tuple[int, int]]):
        """Place mines randomly except safe.cells, find adjacency counts."""
        size = self.board.size
        all_positions = [(r, c) for r in range(size) for c in range(size) if (r, c) not in safe_cells]
        random.shuffle(all_positions)
        for (r, c) in all_positions[: self.board.mine_count]:
            self.board._grid[r][c].is_mine = True
        # adjacency counts
        for r in range(size):
            for c in range(size):
                cell = self.board._grid[r][c]
                if cell.is_mine:
                    continue
                cell.adjacent = sum(1 for nr, nc in self.board.neighbors(r, c) if self.board._grid[nr][nc].is_mine)
        self.board._mines_placed = True

    def _ensure_mines_placed(self, first_r: int, first_c: int):
        """Ensure mines placed with first-click safety around (first_r, first_c)."""
        if self.board._mines_placed:
            return
        safe = {(first_r, first_c)} | set(self.board.neighbors(first_r, first_c))
        self._place_mines(safe)

    def _check_win(self) -> bool:
        """Check win condition: all safe cells are revealed"""
        total_safe = self.board.size * self.board.size - self.board.mine_count
        if self._revealed_safe_cells == total_safe:
            self.status = GameStatus.WON
            return True
        return False

    def remaining_flags(self) -> int:
        return self.board.mine_count - self.flags_placed

    def reveal(self, coord: str) -> Tuple[bool, str]:
        if self.status != GameStatus.PLAYING:
            return False, "Game already over."
        parsed = self.board.parse_coord(coord)
        if not parsed:
            return False, "Invalid. Example: A1 or J10."
        r, c = parsed
        cell = self.board._grid[r][c]
        if cell.is_flagged:
            return False, "Cell is flagged. Unflag first."
        if cell.is_revealed:
            # Chording attempt if it's a numbered cell
            if cell.adjacent > 0:
                return self._chord(r, c)
            return False, "Cell already revealed."
        hit_mine = self._reveal_cell(r, c)
        if hit_mine:
            self.status = GameStatus.LOST
            return True, "Mine hit"
        if self._check_win():
            return False, "All safe cells revealed."
        return False, "Cell revealed."

    def _chord(self, r: int, c: int) -> Tuple[bool, str]:
        """"Auto-reveal hidden neighbors if correctly flagged numbered cell adj mines"""
        cell = self.board._grid[r][c]
        flags = 0
        hidden_neighbors: List[Tuple[int, int]] = []
        for nr, nc in self.board.neighbors(r, c):
            ncell = self.board._grid[nr][nc]
            if ncell.is_flagged:
                flags += 1
            elif not ncell.is_revealed:
                hidden_neighbors.append((nr, nc))
        if flags != cell.adjacent:
            return False, "No chording, flag count mismatch."  # not enough flags
        # Reveal all hidden neighbors
        for nr, nc in hidden_neighbors:  # auto-reveal each remaining covered neighbor
            if self._reveal_cell(nr, nc):
                self.status = GameStatus.LOST
                return True, "Mine hit during chording."
        if self._check_win():
            return False, "All safe cells revealed."
        return False, "Chording reveal complete."

    def toggle_flag(self, coord: str) -> str:
        if self.status != GameStatus.PLAYING:
            return "Game already finished."
        parsed = self.board.parse_coord(coord)
        if not parsed:
            return "Invalid. Example: A1 or J10."
        r, c = parsed
        cell = self.board._grid[r][c]
        if cell.is_revealed:
            return "Can't flag a revealed cell."
        if not cell.is_flagged and self.flags_placed >= self.board.mine_count:
            return "No flags remaining."
        was_flagged = cell.is_flagged
        if was_flagged:
            cell.is_flagged = False
            self.flags_placed -= 1
            return "Flag removed."
        else:
            cell.is_flagged = True
            self.flags_placed += 1
            return "Flag placed."

    def status_line(self) -> str:
        """Game status print"""
        return f"Status: {self.status.value} | Remaining Flags: {self.remaining_flags()}"

    def render(self) -> str:
        reveal_mines = self.status == GameStatus.LOST
        return self.board.render(reveal_mines=reveal_mines)
