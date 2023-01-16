from typing import List, Dict, Tuple
from src.lib.mathematical_land import Vector

ALLOWED_MOVES = [
    Vector(1, 2),
    Vector(-1, 2),
    Vector(2, 1),
    Vector(-2, 1),
    Vector(1, -2),
    Vector(-1, -2),
    Vector(2, -1),
    Vector(-2, -1),
]


class Cell:
    def __init__(self, position):
        self.position = position
        self.min_moves = None
        self.prev_cell = None
        self.planted = False

    def plant_flag(self, min_moves, prev_cell):
        if not self.planted:
            self.min_moves = min_moves
            self.prev_cell = prev_cell
            self.planted = True
            return

        raise Exception("Flag Conflict!")

    def __repr__(self):
        return f"Cell{self.position.i_xy}"


class Board:
    def __init__(self, rows: int, columns: int, obstacles: List[Vector], target: Vector, horse: Vector):
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.target = target
        self.horse = horse

        self.cells: Dict[Tuple[int, int], Cell] = self.calc_available_cells()
        self.unplanted_cells: List[Tuple[int, int]] = list(self.cells.keys())

        self.plant()

    def out_of_bounds(self, point: Vector):
        return not ((0 <= point.x < self.columns) and (0 <= point.y < self.rows))

    def calc_next_moves(self, start: Vector) -> List[Vector]:
        moves = []
        for move in ALLOWED_MOVES:
            end = start + move
            if self.out_of_bounds(end) or end in self.obstacles or end.i_xy not in self.unplanted_cells:
                continue
            moves.append(end)
        return moves

    def calc_available_cells(self):
        cells = {}

        for y in range(self.rows):
            for x in range(self.columns):
                cell = Vector(x, y)
                if cell in self.obstacles:
                    continue
                cells[(x, y)] = Cell(cell)

        del cells[self.horse.xy]
        return cells

    def plant_cells(self, cells, count, prev_cell):
        for cell in cells:
            if cell.i_xy not in self.unplanted_cells:
                continue
            self.cells[cell.xy].plant_flag(count, prev_cell)
            self.unplanted_cells.remove(cell.i_xy)

    def plant(self):
        last_buffer = self.calc_next_moves(self.horse)
        self.plant_cells(last_buffer, 1, self.horse)

        count = 2
        while self.target.xy in self.unplanted_cells:
            buffer = []
            for move in last_buffer:
                next_moves = self.calc_next_moves(move)
                self.plant_cells(next_moves, count, self.cells[move.i_xy])
                buffer += next_moves
            last_buffer = buffer
            count += 1

    def solve(self):
        path = [self.cells[self.target.i_xy]]
        while type(path[-1].prev_cell) is Cell:
            path.append(path[-1].prev_cell)
        return path


if __name__ == "__main__":
    board = Board(8, 8, [Vector(5, 5)], Vector(0, 0), Vector(7, 7))
    print(board.solve())
