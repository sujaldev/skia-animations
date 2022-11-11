from lib.mathematical_land import Circle, Vector
from lib.ui_backend import Window
from skia import Canvas, Color
from math import pi

ring = Circle(
    Vector(500, 500, 0),
    100, pi/2, 0
)


def event_loop(canvas: Canvas, event):
    canvas.drawColor(Color(0, 0, 0))

    if event.window.data1 == 79:
        ring.z_rotation += .05
    elif event.window.data1 == 80:
        ring.z_rotation -= .05
    elif event.window.data1 == 82:
        ring.x_rotation += .05
    elif event.window.data1 == 81:
        ring.x_rotation -= .05

    ring.paint(canvas, 3, Color(0, 255, 0))


window = Window("Simple Ring", 1920, 1080, event_loop=event_loop)
window.start()
