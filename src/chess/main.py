import skia

from src.chess.ui_backend import Window
from src.lib.mathematical_land import Vector
from src.chess.renderer import ChessBoard, Horse
from src.chess.solver import Board

board = ChessBoard()
horse = Horse(board)
# noinspection PyArgumentList
solver = Board(board.rows, board.columns, [Vector(*o) for o in board.obstacles], Vector(*board.target), horse.position)
path = solver.solve()
start = horse
paint = skia.Paint(Color=skia.Color(0, 255, 0))


def frame_renderer(canvas: skia.Canvas, time):
    global start

    board.paint(canvas)
    horse.paint(canvas)

    if path:
        end = path.pop()
        canvas.drawLine(
            start.position.x * 100 + 50, start.position.y * 100 + 50,
            end.position.x * 100 + 50, end.position.y * 100 + 50,
            paint
        )
        canvas.drawCircle(
            start.position.x * 100 + 50, start.position.y * 100 + 50,
            15, paint
        )
        canvas.drawCircle(
            end.position.x * 100 + 50, end.position.y * 100 + 50,
            15, paint
        )
        start = end


window = Window("Raj's Question", 800, 800)
window.frame_renderer = frame_renderer
window.main_loop()
