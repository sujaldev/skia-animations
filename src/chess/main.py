import math
from random import randint

from src.chess.ui_backend import Window
from src.lib.mathematical_land import Vector
from src.chess.renderer import ChessBoard, Horse

board = ChessBoard()
horse = Horse(board)


def frame_renderer(canvas, time):
    board.paint(canvas)
    horse.paint(canvas)


window = Window("Raj's Question", 800, 800)
window.frame_renderer = frame_renderer
window.main_loop()
