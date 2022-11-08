from lib.mathematical_land import Cube, Vector, Square3D
from lib.ui_backend import Window
from skia import Canvas, Color

main_cube = Cube(
    Vector(500, 500, 0),
    0, 0, 200
)

base_plane = Square3D(
    Vector(300, 500, 500), 0, 0, 500
)


def event_loop(canvas: Canvas, event):
    canvas.drawColor(Color(0, 0, 0))

    if event.window.data1 == 79:
        main_cube.y_rotation += .05
        base_plane.y_rotation -= .05
    elif event.window.data1 == 80:
        main_cube.y_rotation -= .05
        base_plane.y_rotation += .05
    elif event.window.data1 == 82:
        main_cube.x_rotation += .05
        base_plane.x_rotation -= .05
    elif event.window.data1 == 81:
        main_cube.x_rotation -= .05
        base_plane.x_rotation += .05

    main_cube.paint(canvas, 3, Color(0, 255, 0))
    base_plane.paint(canvas, 1, Color(255, 0, 0))


window = Window("Simple Cube", 1000, 1000, event_loop=event_loop)
window.start()
