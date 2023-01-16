from math import floor
from random import randint, choice

from src.lib.mathematical_land import Vector

import skia

CELL_SIZE = 100
ROWS, COLUMNS = 8, 8
BLACK, WHITE = skia.Color(0, 0, 0), skia.Color(255, 255, 255)


class Square:
    def __init__(self, size: int, position: Vector, color: skia.Color):
        self.size = size
        self.position = position  # position vector of top left point of square
        self.color = color

    def paint(self, canvas: skia.Canvas):
        bottom_right = self.position + Vector(self.size, self.size)
        # noinspection PyTypeChecker
        canvas.drawRect(
            skia.Rect(*self.position.xy, *bottom_right.xy),
            skia.Paint(Color=self.color)
        )


class Horse:
    PADDING = 20

    def __init__(self, board: "ChessBoard", position: Vector = None):
        self.board = board
        self.position = position
        if self.position is None:
            self.position = Vector(*choice(self.board.available_cells))

        self.color = skia.Color(0, 255, 0)

    @property
    def coordinates(self):
        x, y = self.position.xy
        top_right = Vector(CELL_SIZE * x + self.PADDING, CELL_SIZE * y + self.PADDING)
        bottom_right = top_right + Vector(CELL_SIZE - 2 * self.PADDING, CELL_SIZE - 2 * self.PADDING)
        return *top_right.xy, *bottom_right.xy

    @property
    def corners(self):
        # noinspection PyTupleAssignmentBalance
        x1, y1, x2, y2 = self.coordinates
        return (x1, y1), (x2, y1), (x1, y2), (x2, y2)

    @property
    def dirty_cells(self):
        # cells currently below the horse, should be repainted next frame
        dirty_cells = []
        for x, y in self.corners:
            dirty_cells.append((
                floor(x / CELL_SIZE),
                floor(y / CELL_SIZE)
            ))
        return dirty_cells

    def paint(self, canvas: skia.Canvas):
        self.board.dirty_cells = self.dirty_cells

        # noinspection PyTypeChecker
        canvas.drawRect(
            skia.Rect(*self.coordinates),
            skia.Paint(Color=self.color)
        )


class ChessBoard:
    OBSTACLE_MIN, OBSTACLE_MAX = 8, 16  # both ends inclusive
    # OBSTACLE_COLOR = skia.Color(255, 0, 0)
    OBSTACLE_COLOR = skia.Color(65, 65, 65)
    TARGET_COLOR = skia.Color(0, 0, 255)

    def __init__(self, rows=8, columns=8):
        self.rows = rows
        self.columns = columns
        self.dirty = True  # this will only be true once, false after first paint of the entire board.
        self.dirty_cells = []

        self.obstacles = self.generate_obstacles()
        self.target = self.random_cell
        if self.target in self.obstacles:
            self.obstacles.remove(self.target)

        self.squares = self.generate_board()

    def generate_obstacles(self):
        return [self.random_cell for _ in range(randint(self.OBSTACLE_MIN, self.OBSTACLE_MAX))]

    @property
    def random_cell(self):
        return randint(0, self.columns - 1), randint(0, self.rows - 1)

    @property
    def available_cells(self):
        return [cell for cell in self.squares if cell not in self.obstacles + [self.target]]

    def cell_color(self, x, y, fallback):
        if (x, y) in self.obstacles:
            return self.OBSTACLE_COLOR
        elif (x, y) == self.target:
            return self.TARGET_COLOR
        return fallback

    def generate_board(self):
        board = {}
        start_color = BLACK  # that is the color of the first box in a row.

        for y in range(self.rows):
            column_color = start_color

            for x in range(self.columns):
                board[(x, y)] = Square(
                    CELL_SIZE, Vector(CELL_SIZE * x, CELL_SIZE * y),
                    self.cell_color(x, y, column_color),
                )
                column_color = swap_color(column_color)

            start_color = swap_color(start_color)

        return board

    def redraw_dirty_cells(self, canvas: skia.Canvas):
        for cell in self.dirty_cells:
            if cell in self.squares:
                self.squares[cell].paint(canvas)

    def paint(self, canvas: skia.Canvas):
        self.redraw_dirty_cells(canvas)

        if not self.dirty:
            return

        for square in self.squares.values():
            square.paint(canvas)

        self.dirty = False


def swap_color(color: skia.Color):
    if color == BLACK:
        return WHITE
    return BLACK
